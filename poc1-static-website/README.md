# POC 1: Static Website on Azure Storage

Personal portfolio website hosted on Azure Blob Storage using static website hosting.

## 🌐 Live Demo

**Website:** [https://YOUR-STORAGE-ACCOUNT.z13.web.core.windows.net/](https://vipalst1.z29.web.core.windows.net/)

## 🎯 What I Built

- Responsive portfolio website (HTML/CSS/JavaScript)
- Hosted on Azure Blob Storage with static website feature
- Custom styling with Azure blue theme
- Smooth scrolling navigation

## Architecture

```
User Browser
     ↓
Azure Storage Account (Static Website Enabled)
     ↓
$web Container (Public Blob Access)
     ↓
index.html + style.css + script.js
```

**Stack:** HTML5, CSS3, JavaScript, Azure Storage

## 📸 Screenshots

### Live Website

![Website](./screenshots/website-live.png)

### Azure Storage Configuration

![Storage](./screenshots/azure-storage-overview.png)

### Files in $web Container

![Files](./screenshots/web-container-files.png)

## 💡 What I Learned

**Azure Concepts:**

- Azure Storage Accounts and their configuration
- Static website hosting feature in Blob Storage
- Storage containers and blob access levels
- Storage redundancy options (LRS vs GRS)
- Cost optimization with LRS tier

**Web Development:**

- Responsive design with CSS
- Smooth scrolling with JavaScript
- HTML5 semantic markup
- Deploying static sites to cloud

**Key Insight:** Static website hosting is incredibly cheap (~$1-2/month) for portfolios and documentation sites with no backend needs.

## Cost

**Monthly:** ~$1-2
**Breakdown:** Storage $0.02 + Bandwidth $0.50-1.00
**vs Traditional Hosting:** $5-15/month savings

## Deployment

Created Storage Account → Enabled Static Website → Uploaded files to $web container via Azure Portal.

Source code: [src/](./src/)

---

**Time:** 2 hours | **Difficulty:** Beginner | **Cost:** $1-2/month
