import { GitPullRequest, Webhook, FileCode, Bot, CheckCircle } from "lucide-react";

const steps = [
  {
    icon: GitPullRequest,
    title: "PR Created",
    description: "Developer opens a Pull Request on GitHub",
  },
  {
    icon: Webhook,
    title: "Webhook Triggered",
    description: "GitHub sends event to FastAPI endpoint",
  },
  {
    icon: FileCode,
    title: "Fetch Diff",
    description: "Backend fetches code changes via GitHub API",
  },
  {
    icon: Bot,
    title: "AI Analysis",
    description: "OpenAI reviews code for issues",
  },
  {
    icon: CheckCircle,
    title: "Feedback Returned",
    description: "Structured JSON response with findings",
  },
];

export function FlowDiagram() {
  return (
    <div className="relative">
      {/* Connection line */}
      <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-to-r from-primary/20 via-primary to-primary/20 hidden lg:block" />
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
        {steps.map((step, index) => (
          <div
            key={index}
            className="relative flex flex-col items-center text-center animate-fade-in"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <div className="relative z-10 w-16 h-16 rounded-2xl bg-card border-2 border-primary/30 flex items-center justify-center mb-4 shadow-lg">
              <step.icon className="w-7 h-7 text-primary" />
            </div>
            <h3 className="font-semibold text-foreground mb-1">{step.title}</h3>
            <p className="text-sm text-muted-foreground">{step.description}</p>
            
            {/* Step number */}
            <div className="absolute -top-2 -right-2 w-6 h-6 rounded-full bg-primary text-primary-foreground text-xs font-bold flex items-center justify-center">
              {index + 1}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
