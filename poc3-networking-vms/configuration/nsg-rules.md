# Network Security Group Rules - Complete Reference

## NSG: nsg-public (Frontend VM)

### Inbound Rules

| Priority | Name                          | Source            | Source Port | Destination    | Dest Port | Protocol | Action | Purpose                         |
| -------- | ----------------------------- | ----------------- | ----------- | -------------- | --------- | -------- | ------ | ------------------------------- |
| 100      | Allow-HTTP-Inbound            | Internet          | *           | *              | 80        | TCP      | Allow  | Web traffic from internet       |
| 110      | Allow-HTTPS-Inbound           | Internet          | *           | *              | 443       | TCP      | Allow  | Secure web traffic (future SSL) |
| 120      | Allow-SSH-MyIP                | 106.222.201.x/32  | *           | *              | 22        | TCP      | Allow  | Admin SSH from my IP only       |
| 65000    | AllowVnetInBound              | VirtualNetwork    | *           | VirtualNetwork | *         | Any      | Allow  | Default: inter-VNet traffic     |
| 65001    | AllowAzureLoadBalancerInBound | AzureLoadBalancer | *           | *              | *         | Any      | Allow  | Default: health probes          |
| 65500    | DenyAllInBound                | *                 | *           | *              | *         | Any      | Deny   | Default: deny all other inbound |

### Outbound Rules

| Priority | Name                  | Source         | Source Port | Destination    | Dest Port | Protocol | Action | Purpose                                 |
| -------- | --------------------- | -------------- | ----------- | -------------- | --------- | -------- | ------ | --------------------------------------- |
| 100      | Allow-Backend-API     | 10.0.1.0/24    | *           | 10.0.2.0/24    | 5000      | TCP      | Allow  | Frontend can reach backend API          |
| 65000    | AllowVnetOutBound     | VirtualNetwork | *           | VirtualNetwork | *         | Any      | Allow  | Default: inter-VNet traffic             |
| 65001    | AllowInternetOutBound | *              | *           | Internet       | *         | Any      | Allow  | Default: outbound to internet (updates) |
| 65500    | DenyAllOutBound       | *              | *           | *              | *         | Any      | Deny   | Default: deny all other outbound        |

### Notes

**Why allow HTTP/HTTPS from Internet?**
- This is the frontend - needs to serve web traffic
- Users access via public IP

**Why restrict SSH to /32?**
- Maximum security - only my exact IP can administer
- Prevents brute-force attacks from internet
- Must update when home IP changes

**Why allow outbound to backend?**
- Frontend needs to proxy API requests to backend
- Specific port (5000) and destination (10.0.2.0/24)

**Why allow outbound to Internet?**
- For apt updates and package installs
- Could be restricted with Private Endpoints (more complex)

---

## NSG: nsg-private (Backend VM)

### Inbound Rules

| Priority | Name                          | Source            | Source Port | Destination    | Dest Port | Protocol | Action | Purpose                                    |
| -------- | ----------------------------- | ----------------- | ----------- | -------------- | --------- | -------- | ------ | ------------------------------------------ |
| 100      | Allow-API-From-Frontend       | 10.0.1.0/24       | *           | *              | 5000      | TCP      | Allow  | Accept API calls from frontend subnet only |
| 110      | Allow-SSH-From-Frontend       | 10.0.1.0/24       | *           | *              | 22        | TCP      | Allow  | SSH via jumpbox (frontend VM)              |
| 120      | Deny-Internet-Inbound         | Internet          | *           | *              | *         | Any      | Deny   | Explicit: block all internet inbound       |
| 65000    | AllowVnetInBound              | VirtualNetwork    | *           | VirtualNetwork | *         | Any      | Allow  | Default: inter-VNet traffic                |
| 65001    | AllowAzureLoadBalancerInBound | AzureLoadBalancer | *           | *              | *         | Any      | Allow  | Default: health probes                     |
| 65500    | DenyAllInBound                | *                 | *           | *              | *         | Any      | Deny   | Default: deny all other inbound            |

### Outbound Rules

| Priority | Name                  | Source         | Source Port | Destination    | Dest Port | Protocol | Action | Purpose                          |
| -------- | --------------------- | -------------- | ----------- | -------------- | --------- | -------- | ------ | -------------------------------- |
| 65000    | AllowVnetOutBound     | VirtualNetwork | *           | VirtualNetwork | *         | Any      | Allow  | Default: inter-VNet traffic      |
| 65001    | AllowInternetOutBound | *              | *           | Internet       | *         | Any      | Allow  | Default: outbound for updates    |
| 65500    | DenyAllOutBound       | *              | *           | *              | *         | Any      | Deny   | Default: deny all other outbound |

### Notes

**Why only allow API from frontend subnet?**

- Backend should never be accessed from internet
- Only frontend VM needs to reach it
- Defense in depth: network-level isolation

**Why allow SSH from frontend subnet?**

- Jumpbox pattern: SSH to frontend, then hop to backend
- Backend has no public IP (can't SSH directly)
- Secure management access

**Why explicitly deny Internet inbound?**
- Redundant (default deny exists) but makes intent clear
- Documentation value
- Defense in depth

**Why allow Internet outbound?**
- Backend needs apt/pip package updates
- Could be disabled for maximum isolation (would need to pre-install everything)
- Trade-off: convenience vs security

---

## Rule Evaluation

### How NSG Rules Work

**Inbound processing:**
1. Azure checks rules in priority order (lowest number first)
2. First matching rule is applied
3. Processing stops (no further rules checked)
4. If no match, default deny applies

**Example inbound packet to frontend:**
```
Packet: Source=203.0.113.50, Dest=10.0.1.4, Port=22
  ↓
Priority 100 (HTTP): Port=80 → No match, continue
Priority 110 (HTTPS): Port=443 → No match, continue
Priority 120 (SSH): Source=106.222.201.x, Port=22 → MATCH!
  ↓ Action: Allow (if source IP matches)
  ↓ Action: Deny (if source IP doesn't match, fall through to default deny)
```

### Common Mistakes Avoided

**Mistake 1: Wrong priority order**
```
❌ Priority 100: Allow SSH from Any
   Priority 200: Deny SSH from Internet
   Result: SSH allowed (rule 100 matches first, rule 200 never evaluated)

✅ Priority 100: Allow SSH from My IP only
   Priority 200: Deny all
   Result: Only my IP can SSH
```

**Mistake 2: Forgetting /32**
```
❌ Source: 106.222.201.0
   Ambiguous - is it single IP or subnet?

✅ Source: 106.222.201.0/32
   Clear - exactly one IP
```

**Mistake 3: Allowing 0.0.0.0/0 for SSH**
```
❌ Source: Any (0.0.0.0/0)
   Exposed to brute-force attacks

✅ Source: 106.222.201.0/32
   Only my IP can connect
```

---

## Testing NSG Rules

### Test 1: Frontend HTTP Access
```bash
# From any internet location
curl http://<VM1-PUBLIC-IP>
# Expected: Success (NSG allows HTTP from Internet)
```

### Test 2: Frontend SSH Access
```bash
# From my IP (106.222.201.x)
ssh azureuser@<VM1-PUBLIC-IP>
# Expected: Success

# From different IP
ssh azureuser@<VM1-PUBLIC-IP>
# Expected: Timeout (NSG blocks)
```

### Test 3: Backend Isolation

```bash
# From internet
curl http://10.0.2.4:5000
# Expected: Timeout (backend has no public IP)

# From frontend VM
ssh azureuser@<VM1-PUBLIC-IP>
curl http://10.0.2.4:5000/api/status
# Expected: Success (NSG allows from frontend subnet)
```

### Test 4: Backend API Access
```bash
# From internet directly
curl http://<VM1-PUBLIC-IP>:5000
# Expected: Timeout (port 5000 not allowed from internet)

# Via reverse proxy
curl http://<VM1-PUBLIC-IP>/api/status
# Expected: Success (Nginx proxies to backend)
```

---

## Security Best Practices Applied

1. **Default Deny:** All traffic denied unless explicitly allowed
2. **Least Privilege:** Only necessary ports and sources allowed
3. **Source Restrictions:** SSH limited to specific IP (/32)
4. **Network Segmentation:** Different rules for public vs private subnets
5. **Defense in Depth:** NSG + no public IP on backend + jumpbox pattern
6. **Explicit Rules:** Clear naming and documentation

## Compliance Considerations

**CIS Azure Foundations Benchmark:**
- ✅ NSGs configured for all subnets
- ✅ SSH access restricted (not 0.0.0.0/0)
- ✅ Unused ports closed
- ✅ Explicit rules (not relying only on defaults)

**SOC 2 / ISO 27001:**
- ✅ Network segmentation implemented
- ✅ Least privilege access control
- ✅ Audit trail (NSG changes logged)

---

**Note:** These NSG rules are for POC/learning purposes. Production deployments should additionally consider: NSG Flow Logs, Azure Firewall, Web Application Firewall (WAF), DDoS Protection, and integration with Azure Security Center.
