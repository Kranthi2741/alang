"""
Tool system for Alang - File operations and utilities
"""

import os
import shutil
import subprocess
import glob
from pathlib import Path
from typing import Dict, List, Optional, Any
import json


class Tool:
    """Base class for all tools"""
    
    def __init__(self):
        self.name = self.__class__.__name__.lower().replace('tool', '')
        self.description = self.__doc__ or "No description available"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given arguments
        
        Returns:
            Dictionary with 'success', 'result', and 'error' keys
        """
        raise NotImplementedError("Tool must implement execute method")


class ReadFileTool(Tool):
    """Read the contents of a file"""
    
    def execute(self, filename: str, **kwargs) -> Dict[str, Any]:
        """Read file contents"""
        try:
            if not os.path.exists(filename):
                return {
                    "success": False,
                    "error": f"File '{filename}' not found"
                }
            
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "success": True,
                "result": content,
                "lines": len(content.splitlines()),
                "size": len(content)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read file '{filename}': {str(e)}"
            }


class WriteFileTool(Tool):
    """Write content to a file"""
    
    def execute(self, filename: str, content: str, **kwargs) -> Dict[str, Any]:
        """Write content to file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "success": True,
                "result": f"Successfully wrote {len(content)} characters to '{filename}'"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to write file '{filename}': {str(e)}"
            }


class ListFilesTool(Tool):
    """List files in a directory"""
    
    def execute(self, directory: str = ".", show_hidden: bool = False, **kwargs) -> Dict[str, Any]:
        """List files in directory"""
        try:
            if not os.path.exists(directory):
                return {
                    "success": False,
                    "error": f"Directory '{directory}' not found"
                }
            
            files = []
            directories = []
            
            for item in os.listdir(directory):
                if not show_hidden and item.startswith('.'):
                    continue
                
                item_path = os.path.join(directory, item)
                
                if os.path.isdir(item_path):
                    directories.append(f"{item}/")
                else:
                    size = os.path.getsize(item_path)
                    files.append(f"{item} ({size} bytes)")
            
            result = []
            if directories:
                result.append("📁 Directories:")
                result.extend(f"  {d}" for d in sorted(directories))
            
            if files:
                if result:
                    result.append("")
                result.append("📄 Files:")
                result.extend(f"  {f}" for f in sorted(files))
            
            return {
                "success": True,
                "result": "\\n".join(result) if result else "Empty directory",
                "files_count": len(files),
                "directories_count": len(directories)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to list directory '{directory}': {str(e)}"
            }


class SearchFilesTool(Tool):
    """Search for files matching a pattern"""
    
    def execute(self, pattern: str, directory: str = ".", **kwargs) -> Dict[str, Any]:
        """Search for files matching pattern"""
        try:
            search_pattern = os.path.join(directory, pattern)
            matches = glob.glob(search_pattern, recursive=True)
            
            if not matches:
                return {
                    "success": True,
                    "result": f"No files found matching pattern '{pattern}' in '{directory}'"
                }
            
            result = [f"Found {len(matches)} files matching '{pattern}':"]
            for match in sorted(matches):
                if os.path.isfile(match):
                    size = os.path.getsize(match)
                    result.append(f"  📄 {match} ({size} bytes)")
                else:
                    result.append(f"  📁 {match}/")
            
            return {
                "success": True,
                "result": "\\n".join(result),
                "matches": matches
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to search files: {str(e)}"
            }


class SearchInFilesTool(Tool):
    """Search for text within files"""
    
    def execute(self, text: str, directory: str = ".", file_pattern: str = "*", **kwargs) -> Dict[str, Any]:
        """Search for text within files"""
        try:
            import re
            
            search_pattern = os.path.join(directory, "**", file_pattern)
            files = glob.glob(search_pattern, recursive=True)
            
            matches = []
            total_matches = 0
            
            for file_path in files:
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                        
                        file_matches = []
                        for line_num, line in enumerate(lines, 1):
                            if re.search(re.escape(text), line, re.IGNORECASE):
                                file_matches.append(f"  Line {line_num}: {line.strip()}")
                                total_matches += 1
                        
                        if file_matches:
                            matches.append(f"📄 {file_path}:")
                            matches.extend(file_matches)
                            matches.append("")
                    
                    except (UnicodeDecodeError, PermissionError):
                        # Skip binary files or files we can't read
                        continue
            
            if not matches:
                return {
                    "success": True,
                    "result": f"No matches found for '{text}' in {directory}"
                }
            
            result = [f"Found {total_matches} matches for '{text}':"]
            result.extend(matches)
            
            return {
                "success": True,
                "result": "\\n".join(result),
                "total_matches": total_matches
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to search in files: {str(e)}"
            }


class ExecuteCommandTool(Tool):
    """Execute shell commands"""
    
    def execute(self, command: str, working_directory: str = ".", **kwargs) -> Dict[str, Any]:
        """Execute shell command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=working_directory,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            output = []
            if result.stdout:
                output.append("STDOUT:")
                output.append(result.stdout)
            
            if result.stderr:
                output.append("STDERR:")
                output.append(result.stderr)
            
            output.append(f"Return code: {result.returncode}")
            
            return {
                "success": result.returncode == 0,
                "result": "\\n".join(output),
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Command timed out after 30 seconds: {command}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to execute command '{command}': {str(e)}"
            }


class ToolRegistry:
    """Registry for managing tools"""
    
    def __init__(self):
        self.tools = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default tools"""
        default_tools = [
            ReadFileTool(),
            WriteFileTool(),
            ListFilesTool(),
            SearchFilesTool(),
            SearchInFilesTool(),
            ExecuteCommandTool()
        ]
        
        for tool in default_tools:
            self.register(tool)
    
    def register(self, tool: Tool):
        """Register a new tool"""
        self.tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, str]]:
        """List all available tools"""
        return [
            {
                "name": name,
                "description": tool.description
            }
            for name, tool in self.tools.items()
        ]
    
    def execute_tool(self, name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool by name"""
        tool = self.get_tool(name)
        if not tool:
            return {
                "success": False,
                "error": f"Tool '{name}' not found"
            }
        
        return tool.execute(**kwargs)


# Global tool registry instance
tool_registry = ToolRegistry()
