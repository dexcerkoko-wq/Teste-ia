from mcp.server.fastmcp import FastMCP
import subprocess, tempfile, os

mcp = FastMCP("py-compiler")

@mcp.tool()
def compile_python(code: str) -> str:
    """Compila código Python e retorna o executável em base64."""
    import base64

    with tempfile.TemporaryDirectory() as tmpdir:
        script = os.path.join(tmpdir, 'script.py')
        with open(script, 'w') as f:
            f.write(code)

        result = subprocess.run(
            ['pyinstaller', '--onefile',
             '--distpath', tmpdir,
             '--workpath', os.path.join(tmpdir, 'build'),
             '--specpath', tmpdir,
             script],
            cwd=tmpdir,
            capture_output=True, text=True
        )

        exe = os.path.join(tmpdir, 'script')
        if not os.path.exists(exe):
            return f"Erro na compilação:\n{result.stderr}"

        with open(exe, 'rb') as f:
            return base64.b64encode(f.read()).decode()

if __name__ == '__main__':
    mcp.run(transport="streamable-http")
