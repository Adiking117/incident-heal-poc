from fastmcp import FastMCP
import subprocess

mcp = FastMCP("IncidentOps")

@mcp.tool()
def restartdockercontainer(container_name: str) -> str:
    """Restart a Docker container by name"""
    try:
        # Suppress stdout/stderr so Docker messages don't break JSONRPC
        subprocess.run(
            ["docker", "restart", container_name],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return f"Container '{container_name}' restarted successfully."
    except subprocess.CalledProcessError as e:
        return f"Failed to restart container '{container_name}': {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")