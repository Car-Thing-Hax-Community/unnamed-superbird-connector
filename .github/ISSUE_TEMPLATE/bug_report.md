---
name: Bug report
about: Report any exceptions with this template
title: ''
labels: ''
assignees: ''

---

**Describe the error**
A screenshot or copy-paste of the error. Exceptions look like this:

```
~~~~~ Exception Start ~~~~~
Traceback (most recent call last):
  File "/home/user/Desktop/unamed-superbird-connector/utils/wamp/wamp_handler.py", line 236, in function_handler
    return True, resp, with_event, event
           ^^^^
UnboundLocalError: cannot access local variable 'resp' where it is not associated with a value
~~~~~  Exception End  ~~~~~
```
If you see multiple exceptions, send them all in one issue.

**To Reproduce**
Describe what you were doing when the error appeared:
1. Go to '...'
2. Tap on '....'
3. Scroll down to '....'
4. See error

**Desktop:**
 - OS: [e.g. Debian 12]

**Additional context**
Add any other context about the problem here.
