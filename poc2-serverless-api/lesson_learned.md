# POC 2: Lessons Learned

Collection of incidents, breaks, and learning experiences from POC 2 (Serverless API).

## Break #0: Accidental Test Code in Production

**Date:** [February 5, 2026]
**Duration:** ~24 hours
**Severity:** High (Complete service outage)
**Status:** ✅ Resolved

### What Happened

I was thinking, I deployed function, tested it with concurrent request and it is working, But what if it stop working, what are the possible reasons it could stop working,

Another question I had was, will Azure continuosly allow my function to run without any limit? I mean there has to be some kind of limit or threshold right?

I did some reading and found azure has some default timeout settings applied for each function app plan, my function app plan is "Flex Consumption", so i add sleep timer of 5 min in my function.

Redeployed the function with sleep timer for 5min and tested, Azure waited for 5 min and it initiated function cancellation, as timeout was reached with erro code 500

![Error](../poc2-serverless-api/screenshots/image.png)

### Root Cause

Left time.sleep(300) in code from timeout testing session.

 I tested this, how azure respond to timeout value, but later forgot to delete it.

### Detection Process

**Initial symptoms:**
   - I was not able to reach my function URL via web browser as its HTTP function
      https://hellovipal-c4a4deegake9f3a3.centralindia-01.azurewebsites.net/api/hello?name=Azure

**Investigation steps:**
   - Checked my internet is working or not
  -  Checked if there is no firewall/NSG setting applied on function level
  -   Checked if I typed function URL correctly or not
  -   Nothig helped, so I checked App insight and found out about timeout error because of sleep function i added in the code

**Time to identify:**  1 hours

### Impact

**Technical:**
- Function timing out after 3 minutes on every request
- All API calls failing with 500 errors

**Business (if production):**
-   100% service unavailability
  - Loss of user trust
  - Potential revenue impact

**Actual impact (POC environment):**
- Portfolio demo broken for ~24 hours
- Learning opportunity captured ✅

### Resolution

**Fix applied:**
1. Removed `time.sleep(300)` from code
2. Removed unused `import time`
3. Redeployed function
4. Verified successful execution   (Response time - 1 sec)

**Verification:**
- ✅ Function responds successfully
- ✅ No timeout errors in Application Insights
- ✅ Response time within normal range

### Prevention Measures

**Immediate:**
- Created pre-deployment Checklists

- [ ] Remove all test code (sleep, artificial delays, debug statements)
- [ ] Remove unused imports
- [ ] Review all code changes since last deployment
- [ ] Test function locally or in dev environment
- [ ] Deploy to production
- [ ] Verify function responds successfully (smoke test)
- [ ] Check Application Insights for errors (5 min post-deployment)
- [ ] Verify response times are normal


**Long-term:**
- Consider using feature flags for testing instead of code changes
- Use separate dev/test environment for destructive tests
- Implement automated tests that would catch sleep() statements

### Key Takeaways

1. **Always revert test code immediately** - Don't assume you'll remember later
2. **Application Insights is critical for diagnostics** - Logs showed exact issue
3. **Process matters** - Checklists prevent human error
4. **Documentation turns mistakes into learning** - This incident is now a portfolio asset

### Related Incidents
- None yet (this is Break #0)

## Future Breaks

Planned break scenarios:
- Break #1: Security - Testing authentication bypass
- Break #2: Resource exhaustion - Load testing concurrent requests
- Break #3: Dependency failure - Simulating external service outage

[Results will be documented here as experiments are completed]
