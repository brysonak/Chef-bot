import io
import json
import base64
import aiohttp
import discord
from discord.ext import commands

GODBOLT_API = "https://godbolt.org/api"

LANGUAGES = {
    "c":          ("c",          "cg141"),
    "c++":        ("c++",        "g141"),
    "cpp":        ("c++",        "g141"),
    "rust":       ("rust",       "r1820"),
    "go":         ("go",         "gl1221"),
    "python":     ("python",     "python312"),
    "java":       ("java",       "java2100"),
    "haskell":    ("haskell",    "ghc961"),
    "d":          ("d",          "ldc1_37_0"),
    "pascal":     ("pascal",     "fpc331"),
    "fortran":    ("fortran",    "gfortran141"),
    "ada":        ("ada",        "gnat141"),
    "nim":        ("nim",        "nim2020"),
    "zig":        ("zig",        "z0130"),
    "assembly":   ("assembly",   "nasm2_16_01"),
    "asm":        ("assembly",   "nasm2_16_01"),
    "swift":      ("swift",      "swift60"),
    "kotlin":     ("kotlin",     "kotlinc2020"),
    "csharp":     ("csharp",     "dotnet9csc"),
    "c#":         ("csharp",     "dotnet9csc"),
    "fsharp":     ("fsharp",     "dotnet9fsharpc"),
    "f#":         ("fsharp",     "dotnet9fsharpc"),
}


def build_godbolt_url(language_id: str, compiler_id: str, source: str) -> str:
    session = {
        "id": 1,
        "language": language_id,
        "source": source,
        "compilers": [],
        "executors": [
            {
                "compiler": {
                    "id": compiler_id,
                    "libs": [],
                    "options": ""
                },
                "stdin": "",
                "args": ""
            }
        ]
    }
    clientstate = {"sessions": [session]}
    encoded = base64.b64encode(json.dumps(clientstate).encode()).decode()
    encoded = encoded.replace("/", "%2F")
    return f"https://godbolt.org/clientstate/{encoded}"


async def godbolt_compile(compiler_id: str, source: str) -> dict:
    payload = {
        "source": source,
        "compiler": compiler_id,
        "options": {
            "userArguments": "",
            "executeParameters": {
                "args": "",
                "stdin": ""
            },
            "compilerOptions": {
                "executorRequest": True
            },
            "filters": {
                "execute": True
            },
            "tools": [],
            "libraries": []
        },
        "lang": None,
        "allowStoreCodeDebug": True
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{GODBOLT_API}/compiler/{compiler_id}/compile",
            json=payload,
            headers={"Accept": "application/json"}
        ) as resp:
            return await resp.json(content_type=None)


class Compile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="compile")
    async def compile(self, ctx: commands.Context, *, content: str = ""):
        if not content:
            await ctx.send("Usage: `chef compile \\`\\`\\`<language>\\n<code>\\n\\`\\`\\``")
            return

        if "```" not in content:
            await ctx.send("Wrap your code in a fenced code block with the language specified.\nExample:\n\\`\\`\\`c\n#include <stdio.h>\n...\n\\`\\`\\`")
            return

        lines = content.strip().splitlines()

        start = -1
        end = -1
        for i, line in enumerate(lines):
            if line.startswith("```") and start == -1:
                start = i
            elif line.strip() == "```" and start != -1:
                end = i
                break

        if start == -1 or end == -1:
            await ctx.send("Couldn't parse the code block. Make sure it has an opening and closing ` ``` `.")
            return

        lang_tag = lines[start][3:].strip().lower()
        if not lang_tag:
            await ctx.send("You must specify a language after the opening backticks.\nExample: ` ```c `")
            return

        source = "\n".join(lines[start + 1:end])
        if not source.strip():
            await ctx.send("Your code block is empty.")
            return

        if lang_tag not in LANGUAGES:
            supported = ", ".join(sorted(LANGUAGES.keys()))
            await ctx.send(f"Unsupported language `{lang_tag}`.\nSupported: {supported}")
            return

        language_id, compiler_id = LANGUAGES[lang_tag]
        godbolt_url = build_godbolt_url(language_id, compiler_id, source)

        async with ctx.typing():
            try:
                result = await godbolt_compile(compiler_id, source)
            except Exception as e:
                await ctx.send(f"Request to Godbolt failed: {e}")
                return

        stdout_lines = result.get("stdout", [])
        stderr_lines = result.get("stderr", [])
        build_result = result.get("buildResult", {})
        build_stderr = build_result.get("stderr", []) if build_result else []

        output_parts = []

        if build_stderr:
            build_errors = "\n".join(entry.get("text", "") for entry in build_stderr).strip()
            if build_errors:
                output_parts.append(f"[build errors]\n{build_errors}")

        if stdout_lines:
            stdout = "\n".join(entry.get("text", "") for entry in stdout_lines).strip()
            if stdout:
                output_parts.append(stdout)

        if stderr_lines:
            stderr = "\n".join(entry.get("text", "") for entry in stderr_lines).strip()
            if stderr:
                output_parts.append(f"[stderr]\n{stderr}")

        if not output_parts:
            exit_code = result.get("code", result.get("exitCode", "?"))
            output_parts.append(f"(no output, exit code {exit_code})")

        output = "\n\n".join(output_parts)
        link_line = f"\n[view on godbolt](<{godbolt_url}>)"

        if len(output) + len(link_line) + 8 > 1990:
            file_buf = io.BytesIO(output.encode("utf-8"))
            await ctx.send(
                content=link_line.strip(),
                file=discord.File(file_buf, filename="output.txt")
            )
        else:
            await ctx.send(f"```\n{output}\n```{link_line}")


async def setup(bot):
    await bot.add_cog(Compile(bot))