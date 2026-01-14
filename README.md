# Azure POC Projects

Hands-on Azure projects demonstrating practical cloud skills - from foundational services to production-like architectures.

## 🎯 Goal

Build real-world Azure experience through progressively complex projects, covering compute, storage, networking, and security. Each POC is documented with architecture diagrams, cost analysis, and key learnings.

## 🎓 Certifications

- ✅ **Microsoft Certified: Azure Administrator Associate (AZ-104)**
- ✅ **Microsoft Certified: Azure Solutions Architect Expert (AZ-305)**

## 📂 Projects

### [POC 1: Static Website Hosting](./poc1-static-website/)

**Status:** ✅ Complete
**Description:** Personal portfolio website hosted on Azure Blob Storage with static website hosting
**Services:** Azure Storage, Static Website Hosting, CDN-ready
**Key Skills:** Blob storage, static hosting, cost optimization, HTML/CSS/JS deployment
**Cost:** ~$1-2/month
**Live Demo:** [View Website](https://vipalst1.z29.web.core.windows.net/)

---

### [POC 2: Serverless API](./poc2-serverless-api/)

**Status:** ✅ Complete
**Description:** Two HTTP-triggered serverless APIs - greeting service and temperature converter with dual input support (JSON/URL params)
**Services:** Azure Functions (Flex Consumption), Application Insights
**Key Skills:** Serverless architecture, Python Azure SDK, HTTP triggers, anonymous vs function-level auth, API design
**Cost:** $0/month (free tier: 1M requests)
**Live Demo:** [Test API](https://hellovipal-c4a4deegake9f3a3.centralindia-01.azurewebsites.net/api/convert?value=100&from=C&to=F)

---

### [POC 3: Multi-Tier Network Architecture](./poc3-networking-vms/)

**Status:** ✅ Complete
**Description:** Production-like two-tier architecture with Nginx reverse proxy (public subnet) and Flask API backend (private subnet), demonstrating network segmentation and security
**Services:** Virtual Network, Network Security Groups, Virtual Machines (B1s), Public/Private IPs
**Key Skills:** VNet design, CIDR addressing, NSG rules, network isolation, reverse proxy, jumpbox pattern, SSH key auth, defense-in-depth security

**Architecture:**

- Frontend VM (public subnet) - Nginx reverse proxy
- Backend VM (private subnet, no public IP) - Flask API
- Custom NSG rules for traffic control
- Secure inter-VM communication

**Cost:** ~$11/month (if kept running), ~$0.30 for POC (deleted after documentation)
**Status:** Documented with full architecture diagrams, config files, and test plans

---

### POC 4: Coming Soon

**Status:** 🚧 Planned
**Ideas:** Database integration (Azure SQL), Containers (ACI/ACA), or Infrastructure as Code (Bicep/Terraform)

## 📈 Learning Journey

### Phase 1: Foundation (Complete ✅)

**Coverage:** Storage, Serverless Compute, Networking

- ✅ **POC 1** - Azure Storage fundamentals, static hosting
- ✅ **POC 2** - Serverless computing with Azure Functions
- ✅ **POC 3** - Virtual networks, subnets, NSGs, VMs

**Skills Gained:**

- Cloud storage patterns
- Serverless vs traditional compute
- Network security and isolation
- Cost optimization strategies
- Infrastructure deployment

---

### Phase 2: Intermediate (Next ⏳)

**Focus:** Data, Integration, Automation

- ⏳ **POC 4** - Database (Azure SQL or Cosmos DB)
- ⏳ **POC 5** - Containers (Azure Container Instances/Apps)
- ⏳ **POC 6** - Infrastructure as Code (Bicep or Terraform)

**Target Skills:**

- Data persistence and queries
- Container orchestration
- IaC for repeatable deployments
- CI/CD pipelines

---

### Phase 3: Advanced (Future 🔮)

**Focus:** Scalability, Reliability, DevOps

- Microservices architecture
- Kubernetes (AKS)
- High availability & disaster recovery
- Monitoring and observability
- Multi-region deployments

## 💡 What I've Learned

### Azure Services (Hands-on)

- Azure Storage (Blobs, Static Websites)
- Azure Functions (Serverless, HTTP triggers)
- Virtual Networks (VNet, Subnets, NSGs)
- Virtual Machines (Linux, B-series)
- Application Insights (Monitoring)

### Core Concepts

- **Compute:** Serverless vs VMs, right-sizing, cost optimization
- **Networking:** CIDR notation, public/private subnets, NSG rules, network isolation
- **Security:** Defense-in-depth, SSH keys, least privilege, source IP restrictions
- **Architecture:** Multi-tier patterns, reverse proxy, jumpbox access

### Real-World Skills

- Troubleshooting network connectivity
- Managing dynamic IP challenges with NSGs
- Nginx reverse proxy configuration
- Systemd service management
- SSH agent forwarding for secure multi-hop access
- Cost-conscious decision making (Standard HDD vs SSD, B1s vs larger VMs)

### Total Azure Spend

- **POC 1:** ~$1 (ongoing)
- **POC 2:** $0 (free tier)
- **POC 3:** ~$0.30 (built and deleted)
- **Total:** ~$1.30 for 3 complete POCs

*Compared to traditional hosting: ~$50-100/month savings*

## 🏗️ Architecture Patterns Demonstrated

```
POC 1: Static Content Delivery
Internet → Azure Storage (Blob) → Static Website

POC 2: Serverless API
Internet → Azure Functions → JSON Response

POC 3: Multi-Tier Network
Internet → Public Subnet (Frontend) → Private Subnet (Backend)
         NSG Rules ↓                   NSG Rules ↓
         Nginx Proxy                   Flask API
```

## 📚 Documentation Philosophy

Each POC includes:

- **Architecture diagrams** - Visual representation of design
- **README** - Quick overview, scannable in 2-3 minutes
- **Configuration files** - Actual configs used (nginx, scripts, etc.)
- **Screenshots** - Visual proof of implementation
- **Test plans** - Validation and security testing
- **Cost analysis** - Actual costs and optimization decisions
- **Key learnings** - What worked, what didn't, and why

## 🎓 Next Steps

**Immediate:**

- POC 4: Integrate database with existing APIs
- Explore Azure SQL or Cosmos DB
- Implement CRUD operations

**Short-term:**

- Container-based deployments
- Infrastructure as Code (Bicep)
- CI/CD with GitHub Actions

**Long-term:**

- AKS (Kubernetes) cluster
- Microservices architecture
- Multi-region deployment

## 📞 Connect

- **LinkedIn:** [Vipal Gujrathi](https://linkedin.com/in/vipalg)
- **Email:** vipal.gujrathi@hotmail.com
- **GitHub:** This repository

---

*Building in public | Learning by doing | Documenting the journey*

**Last Updated:** January 2026
