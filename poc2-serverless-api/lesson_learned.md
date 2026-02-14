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
- 100% service unavailability
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
- Break #1.5: Secrets Management
- Break #2: Resource exhaustion - Load testing concurrent requests
- Break #3: Dependency failure - Simulating external service outage

[Results will be documented here as experiments are completed]

---

## Break #1: Security Testing - Authentication Bypass

**Date:** February 14, 2026
**Duration:** ~1 hour
**Type:** Security vulnerability assessment
**Status:** ✅ Mitigated

### What We Tested

Public API with anonymous authentication - anyone with the URL could call without restrictions.

### Investigation Process

**Security assessment:**
1. Tested API accessibility from incognito browser ✅ Fully accessible
2. Checked Application Insights for client tracking:
   - Client IPs masked (0.0.0.0) - cannot block by IP
   - Geo-location data inaccurate (showed wrong city)
   - Can track sessions via `operation_Id`
3. Evaluated security control options:
   - IP blocking ❌ No real IPs available
   - Geo-blocking ❌ Location data unreliable
   - API keys ✅ Viable option
   - Rate limiting ⏳ Not tested yet

### Threat Assessment

**Identified risks:**
1. **Cost overrun** - Abuse beyond free tier (1M requests/month)
2. **Reputation damage** - DDoS could make API appear broken
3. **Unauthorized use** - API used without permission

**Decision:** Implement function-level API key authentication

### Resolution

**Changed authentication model:**
- **Before:** `auth_level=func.AuthLevel.ANONYMOUS`
- **After:** `auth_level=func.AuthLevel.FUNCTION`

**Implementation steps:**
1. Modified `function_app.py` to require function-level auth
2. Redeployed function to Azure
3. Retrieved function key from Azure Portal
4. Updated documentation with secured endpoint

**Access pattern:**
```
# Without key (blocked):
GET /api/hello?name=Test
Response: 401 Unauthorized
```
![Error](../poc2-serverless-api/screenshots/poc2-annoymous-auth-not-working.png)

# With key (allowed):
GET /api/hello?name=Test&code=<function_key>
Response: 200 OK
```

![Success_login](../poc2-serverless-api/screenshots/hello_function_with_key.png)

### Verification

- ✅ Anonymous requests return 401 Unauthorized
- ✅ Requests with valid function key return 200 OK
- ✅ Function key managed securely in Azure Portal
- ✅ Demo still accessible (key embedded in shared URLs)

### Key Takeaways

1. **Portal vs Code configuration** - Auth level defined in code overrides portal settings
2. **Client IP limitations** - Azure Functions mask real client IPs (0.0.0.0), making IP-based blocking ineffective
3. **Geo-location unreliability** - IP geolocation databases can be inaccurate, especially for ISPs and mobile carriers
4. **Session tracking works** - Can detect abuse patterns via `operation_Id` even without real IPs
5. **Security vs accessibility trade-off** - Function keys provide security while maintaining demo accessibility (key in URL)

### Production Considerations

For production APIs, consider additional layers:
- Rate limiting per session/key
- Azure API Management for advanced throttling
- Monitoring alerts for unusual traffic patterns
- Key rotation policy
- Separate keys per consumer for tracking and revocation

### Related Incidents
- Break #0: Accidental test code in production

---

## Break #1.5: Accidentally Committing Secrets

**Date:** February 14, 2026
**Type:** Security incident (prevented)
**Status:** ✅ Caught before damage

### What Happened

Attempted to commit actual Azure Function key to public GitHub repository. GitHub Push Protection blocked the commit.

### Why This Matters

**If successful, would have resulted in:**
- Public exposure of API authentication key
- Unauthorized API usage
- Potential cost overrun
- Need for immediate key rotation

### Detection

GitHub secret scanning detected:
- "Azure Function Key" pattern in `README.md`
- "Azure Function Key" pattern in `poc2-serverless-api/README.md`
- **Blocked push automatically**

### Resolution

**Immediate action:**
1. Removed actual key from documentation
2. Used placeholder text instead
3. Added contact information for demo access

**Prevention:**
- Never commit actual secrets to version control
- Use placeholders in documentation
- For demos: Create separate "demo" keys that can be rotated
- Consider using Azure Key Vault for secret management

### Key Takeaways

1. **GitHub Push Protection works** - Saved from accidental exposure
2. **Public repos require extra care** - Assume everything is visible
3. **Demo keys vs production keys** - Separate credentials for different purposes
4. **Documentation security** - READMEs can leak secrets too, not just code

### Related Incidents
- Break #0: Test code in production
- Break #1: Authentication bypass testing
