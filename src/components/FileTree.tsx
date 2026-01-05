import { Folder, FileCode, FileText } from "lucide-react";

interface FileItem {
  name: string;
  type: "file" | "folder";
  children?: FileItem[];
  description?: string;
}

const projectStructure: FileItem[] = [
  {
    name: "ai-code-review-assistant",
    type: "folder",
    children: [
      {
        name: "app",
        type: "folder",
        children: [
          { name: "__init__.py", type: "file", description: "Package initializer" },
          { name: "main.py", type: "file", description: "FastAPI entry point" },
          { name: "webhook.py", type: "file", description: "GitHub webhook handler" },
          { name: "github_client.py", type: "file", description: "Fetch PR diffs" },
          { name: "ai_reviewer.py", type: "file", description: "AI analysis logic" },
          { name: "utils.py", type: "file", description: "Helper functions" },
        ],
      },
      { name: "requirements.txt", type: "file", description: "Dependencies" },
      { name: ".env.example", type: "file", description: "Environment template" },
      { name: "README.md", type: "file", description: "Documentation" },
    ],
  },
];

function FileTreeItem({ item, depth = 0 }: { item: FileItem; depth?: number }) {
  const Icon = item.type === "folder" ? Folder : item.name.endsWith(".py") ? FileCode : FileText;
  const iconColor = item.type === "folder" ? "text-primary" : "text-muted-foreground";

  return (
    <div>
      <div
        className="flex items-center gap-2 py-1.5 hover:bg-muted/50 rounded px-2 transition-colors"
        style={{ paddingLeft: `${depth * 16 + 8}px` }}
      >
        <Icon className={`w-4 h-4 ${iconColor} flex-shrink-0`} />
        <span className="font-mono text-sm text-foreground">{item.name}</span>
        {item.description && (
          <span className="text-xs text-muted-foreground ml-auto hidden sm:block">
            {item.description}
          </span>
        )}
      </div>
      {item.children?.map((child, index) => (
        <FileTreeItem key={index} item={child} depth={depth + 1} />
      ))}
    </div>
  );
}

export function FileTree() {
  return (
    <div className="rounded-lg border border-border bg-card p-4">
      {projectStructure.map((item, index) => (
        <FileTreeItem key={index} item={item} />
      ))}
    </div>
  );
}
