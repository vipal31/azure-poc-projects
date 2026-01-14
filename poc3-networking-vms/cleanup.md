# Cleanup Guide - POC 3

## Overview

This guide covers how to properly delete all resources created in POC 3 to avoid ongoing charges.

**Estimated time:** 2-3 minutes
**Cost after cleanup:** $0/month

---

## ⚠️ Before You Delete

### Checklist

- [ ] Screenshots captured and saved
- [ ] README documentation complete
- [ ] Configuration files backed up (if needed)
- [ ] Code pushed to GitHub
- [ ] Test results documented

**Important:** Deletion is permanent and cannot be undone!

---

## 🗑️ Deletion Options

### Option 1: Delete Entire Resource Group (Recommended) ⭐

**Fastest and safest** - Deletes everything at once.

#### Azure Portal

1. Navigate to **Resource Groups**
2. Click on `rg-networking-poc3`
3. Click **Delete resource group**
4. Type the resource group name to confirm: `rg-networking-poc3`
5. Click **Delete**
6. Wait 2-3 minutes for deletion to complete

#### Azure CLI
```bash
# Delete resource group and all resources
az group delete --name rg-networking-poc3 --yes --no-wait

# Verify deletion (after 2-3 minutes)
az group exists --name rg-networking-poc3
# Should return: false
```

#### PowerShell
```powershell
# Delete resource group
Remove-AzResourceGroup -Name rg-networking-poc3 -Force

# Verify deletion
Get-AzResourceGroup -Name rg-networking-poc3
# Should return error: ResourceGroupNotFound
```

**What gets deleted:**

- ✅ Both VMs (vm-web-frontend, vm-backend)
- ✅ OS Disks (automatically)
- ✅ Network Interfaces (automatically)
- ✅ Public IP (pip-vm-web)
- ✅ Virtual Network (vnet-poc3)
- ✅ Both Subnets (snet-public, snet-private)
- ✅ Both NSGs (nsg-public, nsg-private)
- ✅ Everything else in the resource group

**Time to complete:** 2-3 minutes
**Cost savings:** ~$11/month

---

### Option 2: Delete Individual Resources

**Use this if you want to keep some resources** (e.g., VNet for future use)

#### Delete VMs First

**Portal:**
1. Virtual Machines → Select `vm-web-frontend`
2. Click **Delete**
3. Check: "Delete with disks" and "Delete with network interfaces"
4. Confirm deletion
5. Repeat for `vm-backend`

**CLI:**
```bash
# Delete frontend VM (with disks and NIC)
az vm delete \
  --resource-group rg-networking-poc3 \
  --name vm-web-frontend \
  --yes

# Delete backend VM
az vm delete \
  --resource-group rg-networking-poc3 \
  --name vm-backend \
  --yes
```

**Cost savings:** ~$8/month (VMs gone, network remains)

---

#### Delete Public IP

**Portal:**
1. Public IP addresses → Select `pip-vm-web`
2. Click **Delete**
3. Confirm

**CLI:**
```bash
az network public-ip delete \
  --resource-group rg-networking-poc3 \
  --name pip-vm-web
```

**Cost savings:** Additional ~$3/month

---

#### Delete NSGs (Optional)

**Only if not planning to reuse**

**CLI:**
```bash
# Delete both NSGs
az network nsg delete \
  --resource-group rg-networking-poc3 \
  --name nsg-public

az network nsg delete \
  --resource-group rg-networking-poc3 \
  --name nsg-private
```

---

#### Delete VNet (Optional)

**Only if completely done with networking POC**

**CLI:**
```bash
az network vnet delete \
  --resource-group rg-networking-poc3 \
  --name vnet-poc3
```

---

#### Delete Resource Group (Final Step)

**After deleting all resources manually:**
```bash
az group delete --name rg-networking-poc3 --yes
```

---

## 🛑 Partial Cleanup Options

### Stop VMs (Instead of Delete)

**Use case:** Want to pause costs but keep configuration

**Portal:**
1. Virtual Machines → Select VM
2. Click **Stop**
3. Wait for status: "Stopped (deallocated)"

**CLI:**
```bash
# Stop (deallocate) both VMs
az vm deallocate --resource-group rg-networking-poc3 --name vm-web-frontend
az vm deallocate --resource-group rg-networking-poc3 --name vm-backend
```

**Cost impact:**
- ✅ Saves: Compute costs (~$8/month)
- ⚠️ Still charged: Disk storage (~$4/month), Public IP (~$3/month)
- **New cost:** ~$7/month instead of ~$11/month

**To restart:**
```bash
az vm start --resource-group rg-networking-poc3 --name vm-web-frontend
az vm start --resource-group rg-networking-poc3 --name vm-backend
```

---

### Keep Network, Delete Compute

**Use case:** Want to reuse network architecture for POC 4

**Steps:**
1. Delete both VMs (with disks/NICs)
2. Delete Public IP
3. Keep: VNet, Subnets, NSGs

**Cost:** ~$0/month (VNet/NSGs are free!)

**Benefit:** Faster setup for next POC using same network

---

## 🔍 Verification

### Confirm All Resources Deleted

**Portal:**
```
Resource Groups → rg-networking-poc3
Should show: "Resource group not found"
```

**CLI:**
```bash
# List all resources in resource group (should be empty or error)
az resource list --resource-group rg-networking-poc3 --output table

# Check if resource group exists
az group exists --name rg-networking-poc3
# Should return: false
```

---

### Check for Orphaned Resources

**Sometimes resources get left behind. Check:**

**Orphaned Disks:**

```bash
# List all disks in subscription
az disk list --query "[?resourceGroup=='rg-networking-poc3']" --output table
```

**Orphaned NICs:**
```bash
az network nic list --query "[?resourceGroup=='rg-networking-poc3']" --output table
```

**Orphaned Public IPs:**
```bash
az network public-ip list --query "[?resourceGroup=='rg-networking-poc3']" --output table
```

**If any found, delete them individually.**

---

## 💰 Cost Impact

### Before Cleanup

| Resource                | Monthly Cost   |
| ----------------------- | -------------- |
| VM1 (B1s)               | $4             |
| VM2 (B1s)               | $4             |
| Public IP               | $3             |
| Disks (2× Standard HDD) | $4             |
| VNet + NSGs             | $0             |
| **Total**               | **~$15/month** |

### After Full Cleanup

| Resource  | Monthly Cost |
| --------- | ------------ |
| None      | $0           |
| **Total** | **$0/month** |

**Savings:** $15/month × 12 = **$180/year**

---

## ⏰ Cleanup Schedule Recommendations

### Immediate Cleanup (Recommended for POCs)

**When:** Right after documentation and screenshots

**Why:**

- ✅ Avoid forgetting and incurring charges
- ✅ POC is documented, no need to keep running
- ✅ Can recreate anytime from documentation

**Timeline:**
```
Day 1: Build POC
Day 1: Test and document
Day 1: Take screenshots
Day 1: Push to GitHub
Day 1: DELETE everything ← Do this!
```

---

### Keep for 1 Week (Alternative)

**When:** If showing to others or continuing testing

**Why:**
- ✅ Available for live demos
- ✅ Can make tweaks without rebuilding
- ⚠️ Costs ~$4 for the week

**Timeline:**
```
Day 1: Build and document
Day 1-7: Available for demos/testing
Day 7: DELETE everything
```

**Cost:** ~$1 for 1 week

---

### Stop VMs When Not Using (Middle Ground)

**Pattern:** Stop VMs daily, start when needed

**Commands:**
```bash
# At end of day
az vm deallocate --resource-group rg-networking-poc3 --name vm-web-frontend
az vm deallocate --resource-group rg-networking-poc3 --name vm-backend

# Next morning
az vm start --resource-group rg-networking-poc3 --name vm-web-frontend
az vm start --resource-group rg-networking-poc3 --name vm-backend
```

**Cost:** ~$7/month (disk + IP only)

---

## 🚨 Common Mistakes to Avoid

### ❌ Deleting VMs but forgetting disks
**Result:** Still charged for orphaned disks (~$4/month)
**Fix:** Always check for orphaned resources

### ❌ Deleting resources individually but missing some
**Result:** Lingering charges
**Fix:** Use resource group deletion (Option 1)

### ❌ Stopping VMs instead of deallocating
**Result:** Still charged for compute
**Fix:** Use "Stop" in Portal (auto-deallocates) or `az vm deallocate`

### ❌ Forgetting about the POC
**Result:** Months of unexpected charges
**Fix:** Set calendar reminder or delete immediately

### ❌ Not verifying deletion
**Result:** Resources still running
**Fix:** Always verify with CLI or Portal

---

## 📋 Quick Reference

### One-Command Full Cleanup
```bash
# Azure CLI (fastest)
az group delete --name rg-networking-poc3 --yes --no-wait && \
echo "Deletion initiated. Verify in 3 minutes with: az group exists --name rg-networking-poc3"
```

### Stop All VMs Quickly

```bash
# Stop both VMs
az vm deallocate --ids $(az vm list -g rg-networking-poc3 --query "[].id" -o tsv)
```

### Restart All VMs Quickly

```bash
# Start both VMs
az vm start --ids $(az vm list -g rg-networking-poc3 --query "[].id" -o tsv)
```

---

## 🎓 Best Practices

### For Learning POCs

1. ✅ **Build → Document → Delete** (same day)
2. ✅ Screenshot everything before deletion
3. ✅ Push code/docs to GitHub first
4. ✅ Use resource group deletion (cleanest)
5. ✅ Verify deletion completed

### For Portfolio Demos

1. 🟡 **Keep for 1 week** max (with calendar reminder)
2. 🟡 **Stop VMs** when not actively demoing
3. 🟡 **Delete public IP** if not demoing (save $3/month)
4. ✅ Set Azure Budget Alert at $5/month

### For Continued Learning

1. 🟢 **Keep network infrastructure** (VNet, NSGs)
2. 🟢 **Delete VMs** when done with current experiment
3. 🟢 **Recreate VMs** as needed for next experiment
4. ✅ Document different configurations

---

## 🔔 Set Budget Alerts

**Prevent surprise bills:**

**Portal:**
1. Cost Management + Billing → Budgets
2. Create budget: $5/month
3. Alert threshold: 80% ($4)
4. Email notification: your-email

**CLI:**
```bash
# Create budget alert
az consumption budget create \
  --budget-name poc3-budget \
  --amount 5 \
  --time-grain Monthly \
  --category Cost
```

---

## ❓ FAQ

### Q: Can I recover deleted resources?

**A:** No, deletion is permanent. Always ensure documentation is complete before deleting.

### Q: Will I be charged for the deletion process?

**A:** No, there's no charge for deleting resources.

### Q: How long does deletion take?

**A:** Resource group deletion: 2-3 minutes. Individual resources: 30 seconds each.

### Q: What if deletion fails?

**A:**

1. Check if resources have locks
2. Remove locks: Resource → Locks → Delete lock
3. Retry deletion
4. If still failing, delete resources individually first

### Q: Can I export my configuration before deleting?

**A:** Yes!

```bash
# Export resource group template
az group export --name rg-networking-poc3 > poc3-template.json
```

### Q: Should I delete the resource group from GitHub?

**A:** No! Keep the documentation. Just delete the Azure resources.

---

## ✅ Deletion Checklist

**Before deletion:**

- [ ] All screenshots captured
- [ ] README complete
- [ ] Configuration files saved
- [ ] Code pushed to GitHub
- [ ] Test results documented
- [ ] Architecture diagrams saved

**Deletion steps:**

- [ ] Run: `az group delete --name rg-networking-poc3 --yes`
- [ ] Wait 2-3 minutes
- [ ] Verify: `az group exists --name rg-networking-poc3` returns `false`
- [ ] Check Azure Portal - resource group gone
- [ ] Check Cost Management - no ongoing charges

**After deletion:**

- [ ] Update POC status in main README (if needed)
- [ ] Set reminder to check bill in 24 hours
- [ ] Celebrate cost savings! 🎉

---

**Need help?** Check Azure documentation or reach out!

**Last Updated:** January 2026
