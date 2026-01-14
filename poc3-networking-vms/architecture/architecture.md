# Network Architecture - Detailed Explanation

## Overview

This POC implements a classic two-tier network architecture with network segmentation, demonstrating production-like patterns for web applications on Azure.

## Network Design

### Virtual Network (VNet)

**Address Space:** 10.0.0.0/16 (65,536 IPs)

**Why /16?**
- Provides ample room for growth
- Standard Azure practice for single-region VNets
- Allows for multiple subnets with clear hierarchy

### Subnet Segmentation

#### Public Subnet: 10.0.1.0/24

**Purpose:** Hosts internet-facing resources (frontend VM)

**Characteristics:**

- 256 IPs (251 usable - Azure reserves 5)
- Resources can have public IPs
- NSG allows selective inbound from internet
- Outbound internet access via Azure default NAT

**Resources:**
- vm-web-frontend (10.0.1.4)
- Public IP associated with frontend VM

#### Private Subnet: 10.0.2.0/24

**Purpose:** Hosts internal resources (backend VM)

**Characteristics:**
- 256 IPs (251 usable)
- No public IPs (isolated from internet)
- NSG only allows traffic from public subnet
- Outbound internet for updates (could be restricted)

**Resources:**
- vm-backend (10.0.2.4)
- No public IP (accessed via frontend as jumpbox)

## Traffic Flow

### User → Frontend
```
User (Internet)
  ↓ HTTP/HTTPS
Public IP (20.x.x.x)
  ↓ NSG Check (nsg-public)
  ↓ Allow HTTP (80), HTTPS (443)
VM1: Nginx (10.0.1.4)
  ↓ Serves static content or proxies to backend
```

### Frontend → Backend
```
VM1 (10.0.1.4)
  ↓ HTTP on port 5000
NSG Check (nsg-private)
  ↓ Allow from 10.0.1.0/24 on port 5000
VM2: Flask API (10.0.2.4)
  ↓ Returns JSON response
```

### SSH Access

**To Frontend (Direct):**
```
Admin (106.222.201.x)
  ↓ SSH on port 22
NSG Check (nsg-public)
  ↓ Allow from 106.222.201.x/32 only
VM1 (10.0.1.4)
```

**To Backend (Jumpbox Pattern):**
```
Admin
  ↓ SSH to VM1 with agent forwarding (-A flag)
VM1 (10.0.1.4)
  ↓ SSH to VM2 on internal network
NSG Check (nsg-private)
  ↓ Allow SSH from 10.0.1.0/24
VM2 (10.0.2.4)
```

## Security Model

### Defense in Depth

**Layer 1: Network Segmentation**
- Public and private subnets
- Backend has no public IP
- Forces traffic through controlled entry point (frontend)

**Layer 2: Network Security Groups**
- NSG on each subnet
- Least-privilege rules
- Default deny, explicit allow

**Layer 3: VM-level Security**
- SSH key authentication (no passwords)
- Source IP restrictions (/32 for admin access)
- Minimal services running

**Layer 4: Application Security**
- Nginx reverse proxy (single entry point)
- Flask API only listens on internal interface
- Service accounts with minimal privileges

## Design Decisions

### Why Two Subnets?

**Alternative: Single Subnet**
- ❌ Less secure (no network isolation)
- ❌ Can't use different NSG rules per tier
- ❌ Violates separation of concerns

**Chosen: Two Subnets**
- ✅ Network-level isolation
- ✅ Different security rules per tier
- ✅ Mimics production patterns
- ✅ Easier to audit and troubleshoot

### Why /24 Subnets?

**Alternatives:**

- /28 (16 IPs) - Too small, limits growth
- /16 (65K IPs) - Wasteful, poor organization

**Chosen: /24 (256 IPs)**

- ✅ Azure best practice
- ✅ Room for growth (load balancers, more VMs)
- ✅ Clean IP hierarchy (10.0.1.x, 10.0.2.x)
- ✅ IPs are free in Azure

### Why No Public IP on Backend?

**Benefits:**

- ✅ Reduced attack surface (can't be reached from internet)
- ✅ Forces traffic through frontend (controlled entry)
- ✅ Prevents accidental exposure
- ✅ Lower cost (no public IP charges)

**Trade-offs:**
- ⚠️ Must use jumpbox for SSH access
- ⚠️ Slightly more complex to manage

**Verdict:** Security benefits outweigh convenience trade-offs

### Static vs Dynamic Public IP

**Attempted:** Dynamic IP (to save $3/month)

**Result:** Portal doesn't offer Dynamic for Standard SKU VMs

**Chosen:** Static IP

- ✅ Stable address (doesn't change on reboot)
- ✅ Required for Standard SKU in Portal
- ✅ Better for documentation/demos
- ⚠️ Costs $3/month

**Alternative:** Use CLI for Dynamic (avoided for simplicity)

## Network Address Translation (NAT)

### Outbound Traffic

Both VMs can access internet for updates:

```

VM (10.0.x.4)
  ↓
VNet
  ↓
Azure Default Outbound NAT
  ↓
Internet (appears as Azure datacenter IP)
  ↓
Package repositories, etc.
```

**Why allow outbound?**

- Needed for `apt update`, `pip install`
- Could be restricted with Service Endpoints (more complex)
- Trade-off: Convenience vs maximum isolation

## Scalability Considerations

### Current Limitations

- Single VM per tier (no redundancy)
- No load balancing
- No auto-scaling
- Manual configuration (not IaC)

### Future Enhancements

**For Production:**

- VM Scale Sets for auto-scaling
- Azure Load Balancer for distribution
- Application Gateway for SSL/WAF
- Azure Bastion for secure management
- Private Endpoints for Azure services
- Hub-spoke topology for multiple apps

## IP Address Allocation

### Reserved IPs (Azure)

Each subnet reserves 5 IPs:

- .0: Network address
- .1: Default gateway
- .2, .3: Azure DNS
- .255: Broadcast

**Example for 10.0.1.0/24:**

- Reserved: 10.0.1.0, .1, .2, .3, .255
- Usable: 10.0.1.4 through 10.0.1.254 (251 IPs)

### Current Allocation

**Public Subnet (10.0.1.0/24):**

- 10.0.1.4: vm-web-frontend
- 10.0.1.5-254: Available for growth

**Private Subnet (10.0.2.0/24):**

- 10.0.2.4: vm-backend
- 10.0.2.5-254: Available for growth

## Monitoring & Observability

### Current State

- Azure Platform metrics (CPU, network, disk)
- Boot diagnostics enabled
- NSG flow logs not enabled (costs extra)

### Recommended Additions

- Azure Monitor Logs
- Network Watcher
- NSG Flow Logs
- Application Insights
- Custom metrics from applications

## Compliance & Governance

**Implemented:**

- Network segmentation
- Least-privilege access
- SSH key authentication
- Audit trail via Azure Activity Log

**Missing (for production):**

- Azure Policy enforcement
- Tags for cost allocation
- Resource locks
- Backup strategy
- Disaster recovery plan

## Cost Optimization

**Decisions:**

- B1s (not B2s): 50% cheaper, adequate for POC
- Standard HDD (not SSD): 60% cheaper, acceptable latency
- No Bastion: Saves $140/month
- No NAT Gateway: Uses default outbound (free)
- Delete after documentation: Ongoing cost = $0

## Diagram

```
Internet
   ↓
Public IP (Static: 20.x.x.x)
   ↓
NSG: nsg-public
   ├─ Allow HTTP (80) from Any
   ├─ Allow HTTPS (443) from Any
   └─ Allow SSH (22) from 106.222.201.x/32
   ↓
┌──────────────────────────────────────────────────┐
│ VNet: vnet-poc3 (10.0.0.0/16)                   │
│                                                   │
│  ┌─────────────────────────────────────────┐    │
│  │ Public Subnet: 10.0.1.0/24              │    │
│  │                                          │    │
│  │  ┌────────────────────────────────┐     │    │
│  │  │ vm-web-frontend (10.0.1.4)     │     │    │
│  │  │ - B1s (1 vCPU, 1GB RAM)        │     │    │
│  │  │ - Standard HDD 30GB            │     │    │
│  │  │ - Ubuntu 22.04 LTS             │     │    │
│  │  │ - Nginx reverse proxy          │     │    │
│  │  │ - Public IP attached           │     │    │
│  │  └────────────────────────────────┘     │    │
│  └─────────────────────────────────────────┘    │
│                    ↓                             │
│         Internal routing (port 5000)             │
│                    ↓                             │
│  ┌─────────────────────────────────────────┐    │
│  │ Private Subnet: 10.0.2.0/24             │    │
│  │                                          │    │
│  │  ┌────────────────────────────────┐     │    │
│  │  │ vm-backend (10.0.2.4)          │     │    │
│  │  │ - B1s (1 vCPU, 1GB RAM)        │     │    │
│  │  │ - Standard HDD 30GB            │     │    │
│  │  │ - Ubuntu 22.04 LTS             │     │    │
│  │  │ - Python Flask API:5000        │     │    │
│  │  │ - NO public IP (isolated)      │     │    │
│  │  └────────────────────────────────┘     │    │
│  └─────────────────────────────────────────┘    │
│                    ↑                             │
│  NSG: nsg-private                                │
│    ├─ Allow 5000 from 10.0.1.0/24              │
│    ├─ Allow SSH from 10.0.1.0/24               │
│    └─ Deny all from Internet                    │
└──────────────────────────────────────────────────┘
```

---

**Key Takeaway:** This architecture demonstrates production network patterns while remaining simple enough for learning. It's not production-ready (single VMs, no redundancy), but shows the foundational concepts used in enterprise Azure deployments.
