import { Bot, Github, Zap, Shield, AlertTriangle, Info, Download, ExternalLink } from "lucide-react";
import { CodeBlock } from "@/components/CodeBlock";
import { FileTree } from "@/components/FileTree";
import { FlowDiagram } from "@/components/FlowDiagram";
import { SeverityBadge } from "@/components/SeverityBadge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <header className="relative overflow-hidden border-b border-border">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,hsl(var(--primary)/0.15),transparent_50%)]" />
        <div className="container mx-auto px-4 py-16 md:py-24 relative">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-6 animate-fade-in">
              <Bot className="w-4 h-4" />
              <span>AI-Powered Code Review</span>
            </div>
            
            <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6 animate-fade-in" style={{ animationDelay: "100ms" }}>
              Code Review
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent"> Assistant</span>
            </h1>
            
            <p className="text-lg md:text-xl text-muted-foreground mb-8 max-w-2xl mx-auto animate-fade-in" style={{ animationDelay: "200ms" }}>
              A beginner-friendly Python application that automatically reviews GitHub Pull Requests using AI.
              Built with FastAPI and OpenAI.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in" style={{ animationDelay: "300ms" }}>
              <Button size="lg" className="gap-2" asChild>
                <a href="#setup">
                  <Download className="w-5 h-5" />
                  Get Started
                </a>
              </Button>
              <Button size="lg" variant="outline" className="gap-2" asChild>
                <a href="#structure">
                  <ExternalLink className="w-5 h-5" />
                  View Code
                </a>
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Features */}
      <section className="container mx-auto px-4 py-16">
        <div className="grid md:grid-cols-3 gap-6">
          {[
            {
              icon: Github,
              title: "GitHub Integration",
              description: "Receives webhook events from Pull Requests automatically",
            },
            {
              icon: Zap,
              title: "AI Analysis",
              description: "Uses OpenAI to analyze code for bugs, security issues, and more",
            },
            {
              icon: Shield,
              title: "Structured Feedback",
              description: "Returns categorized issues with severity levels",
            },
          ].map((feature, index) => (
            <Card key={index} className="group hover:border-primary/50 transition-colors animate-fade-in" style={{ animationDelay: `${index * 100}ms` }}>
              <CardHeader>
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
                  <feature.icon className="w-6 h-6 text-primary" />
                </div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">{feature.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-foreground mb-4">How It Works</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            The application follows a simple flow from PR creation to AI-powered feedback
          </p>
        </div>
        <FlowDiagram />
      </section>

      {/* Project Structure */}
      <section id="structure" className="container mx-auto px-4 py-16">
        <div className="grid lg:grid-cols-2 gap-12 items-start">
          <div>
            <h2 className="text-3xl font-bold text-foreground mb-4">Project Structure</h2>
            <p className="text-muted-foreground mb-8">
              Clean, modular architecture with clear separation of concerns. Each file has a specific responsibility.
            </p>
            <FileTree />
          </div>
          
          <div>
            <h3 className="text-xl font-semibold text-foreground mb-4">Output Format</h3>
            <p className="text-muted-foreground mb-6">
              The AI returns structured JSON with severity-classified issues:
            </p>
            <CodeBlock
              language="json"
              filename="response.json"
              code={`{
  "summary": "Found 2 potential issues in the code changes",
  "issues": [
    {
      "severity": "High",
      "message": "Possible SQL injection vulnerability",
      "suggestion": "Use parameterized queries instead"
    },
    {
      "severity": "Medium",
      "message": "Missing input validation",
      "suggestion": "Add validation for user input"
    }
  ]
}`}
            />
            
            <div className="mt-6 flex flex-wrap gap-2">
              <SeverityBadge severity="Critical" />
              <SeverityBadge severity="High" />
              <SeverityBadge severity="Medium" />
              <SeverityBadge severity="Low" />
            </div>
          </div>
        </div>
      </section>

      {/* Setup Instructions */}
      <section id="setup" className="bg-muted/30 border-y border-border">
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold text-foreground mb-4 text-center">Quick Setup</h2>
            <p className="text-muted-foreground mb-12 text-center">
              Get the AI Code Review Assistant running in minutes
            </p>
            
            <div className="space-y-8">
              <div className="animate-slide-in-right" style={{ animationDelay: "0ms" }}>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-sm font-bold">1</div>
                  <h3 className="text-lg font-semibold text-foreground">Clone & Install Dependencies</h3>
                </div>
                <CodeBlock
                  code={`cd ai-code-review-assistant
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt`}
                />
              </div>
              
              <div className="animate-slide-in-right" style={{ animationDelay: "100ms" }}>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-sm font-bold">2</div>
                  <h3 className="text-lg font-semibold text-foreground">Configure Environment</h3>
                </div>
                <CodeBlock
                  code={`cp .env.example .env
# Edit .env and add your API keys:
# - GITHUB_TOKEN
# - OPENAI_API_KEY
# - GITHUB_WEBHOOK_SECRET`}
                />
              </div>
              
              <div className="animate-slide-in-right" style={{ animationDelay: "200ms" }}>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-sm font-bold">3</div>
                  <h3 className="text-lg font-semibold text-foreground">Run the Server</h3>
                </div>
                <CodeBlock code={`uvicorn app.main:app --reload --port 8000`} />
                <p className="text-sm text-muted-foreground mt-3">
                  <Info className="w-4 h-4 inline mr-1" />
                  API docs available at <code className="text-primary">http://localhost:8000/docs</code>
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Manual Testing */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-foreground mb-4 text-center">Test Without GitHub</h2>
          <p className="text-muted-foreground mb-8 text-center">
            Use the manual review endpoint to test the AI reviewer directly
          </p>
          
          <CodeBlock
            language="bash"
            code={`curl -X POST http://localhost:8000/review \\
  -H "Content-Type: application/json" \\
  -d '{"code": "def hello():\\n    password = \\"admin123\\"\\n    print(password)"}'`}
          />
          
          <Card className="mt-8 border-severity-high/30 bg-severity-high/5">
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-severity-high" />
                <CardTitle className="text-lg">Example Response</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <CodeBlock
                language="json"
                code={`{
  "summary": "Security issue detected: hardcoded credentials",
  "issues": [
    {
      "severity": "Critical",
      "message": "Hardcoded password in source code",
      "suggestion": "Use environment variables or a secrets manager"
    }
  ]
}`}
              />
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8">
        <div className="container mx-auto px-4 text-center text-muted-foreground">
          <p className="text-sm">
            Built with FastAPI, OpenAI, and Python. Beginner-friendly code with detailed comments.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
