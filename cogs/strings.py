# A File where all lomg strings are stored

from discord import Embed

run_usage = r"""\`\`\`language
your code
\`​\`​\`
"""

js_close_code = """
const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}
sleep(2000).then(() => {
  window.close();
})

"""

codeblocks_string ="""
\```language
<code>
\```
**Beispiel**
\```python
print("Hello World")
\```
*wird zu*
```python
print("Hello World")
```
"""

latex_help = r"""

**Bruch**
\frac{a}{b}

**Potenzen**
a^{b}

**Wurzeln**
\sqrt[n]{a}

**Neue Zeile**
\newline

"""
