"use client";

import { useEffect, useState, useCallback } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { api } from "@/lib/api";
import { useProjectStore } from "@/stores/project-store";
import {
  Bot, Brain, Lightbulb, Shield, TrendingUp,
  Play, CheckCircle2, XCircle, Clock, Loader2,
  ArrowRight, Network, FileText, Sparkles,
} from "lucide-react";
import { toast } from "sonner";

const AGENTS = [
  { id: "startup_intelligence", label: "Startup Intelligence", icon: Brain, color: "from-blue-500 to-blue-600" },
  { id: "business_strategy", label: "Business Strategy", icon: Lightbulb, color: "from-violet-500 to-violet-600" },
  { id: "investor_critique", label: "Investor Critique", icon: Shield, color: "from-emerald-500 to-emerald-600" },
  { id: "pitch_intelligence", label: "Pitch Intelligence", icon: TrendingUp, color: "from-amber-500 to-amber-600" },
];

const STATUS_ICONS: Record<string, any> = {
  completed: CheckCircle2,
  running: Loader2,
  failed: XCircle,
  pending: Clock,
};

const STATUS_VARIANTS: Record<string, string> = {
  completed: "success",
  running: "warning",
  failed: "destructive",
  pending: "secondary",
};

export default function WorkspacePage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const projectId = searchParams.get("project");
  const { currentProject, fetchProject, isLoading: projectLoading } = useProjectStore();
  const [agentStatuses, setAgentStatuses] = useState<any[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [overallStatus, setOverallStatus] = useState("idle");
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (projectId) {
      fetchProject(Number(projectId));
    }
  }, [projectId]);

  const pollStatus = useCallback(async (id: number) => {
    try {
      const data = await api.get<{ agents: any[]; overall_status: string; progress_percentage: number }>(`/agents/status/${id}`);
      setAgentStatuses(data.agents);
      setOverallStatus(data.overall_status);
      setProgress(data.progress_percentage);

      if (data.overall_status === "running" || data.overall_status === "pending") {
        setTimeout(() => pollStatus(id), 2000);
      } else if (data.overall_status === "completed") {
        setIsRunning(false);
        toast.success("All agents completed!");
        fetchProject(id);
      } else if (data.overall_status === "failed") {
        setIsRunning(false);
        toast.error("Some agents failed");
      }
    } catch {
      setIsRunning(false);
    }
  }, [fetchProject]);

  const handleRunAgents = async () => {
    if (!projectId) return;
    setIsRunning(true);
    setOverallStatus("running");
    setProgress(0);
    try {
      await api.post("/agents/run", { project_id: Number(projectId) });
      setTimeout(() => pollStatus(Number(projectId)), 2000);
      toast.success("Agent execution started");
    } catch (err: any) {
      toast.error(err.message || "Failed to start agents");
      setIsRunning(false);
    }
  };

  if (!projectId) {
    return (
      <div className="flex flex-col items-center justify-center py-32 text-center">
        <Network className="mb-4 h-16 w-16 text-muted-foreground/30" />
        <h2 className="mb-2 text-2xl font-bold">Select a Project</h2>
        <p className="mb-6 text-muted-foreground">Choose a project from the list to run AI agents.</p>
        <Button onClick={() => router.push("/projects")} className="gap-2">
          View Projects <ArrowRight className="h-4 w-4" />
        </Button>
      </div>
    );
  }

  if (projectLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-8 w-64" />
        <div className="grid gap-4 lg:grid-cols-2">
          {[1, 2, 3, 4].map((i) => <Skeleton key={i} className="h-48 rounded-xl" />)}
        </div>
      </div>
    );
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-8">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Agent Workspace</h1>
          <p className="text-muted-foreground">
            {currentProject?.name || "Mission Control"} — {currentProject?.industry || ""}
          </p>
        </div>
        <div className="flex items-center gap-3">
          {overallStatus === "completed" && (
            <Button variant="outline" className="gap-2" onClick={() => router.push(`/reports?project=${projectId}`)}>
              <FileText className="h-4 w-4" /> View Reports
            </Button>
          )}
          <Button
            size="lg"
            className="gap-2"
            onClick={handleRunAgents}
            disabled={isRunning}
          >
            {isRunning ? (
              <><Loader2 className="h-4 w-4 animate-spin" /> Running...</>
            ) : (
              <><Play className="h-4 w-4" /> Run Agents</>
            )}
          </Button>
        </div>
      </div>

      {(isRunning || overallStatus !== "idle") && (
        <Card className="border-border/50">
          <CardContent className="p-6">
            <div className="mb-2 flex items-center justify-between">
              <span className="text-sm font-medium">Overall Progress</span>
              <span className="text-sm text-muted-foreground">{Math.round(progress)}%</span>
            </div>
            <div className="h-2 overflow-hidden rounded-full bg-muted">
              <motion.div
                className="h-full rounded-full bg-gradient-to-r from-primary via-secondary to-primary"
                initial={{ width: "0%" }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
            <div className="mt-4 flex items-center gap-2">
              <Badge variant={STATUS_VARIANTS[overallStatus] as any || "secondary"}>
                {overallStatus}
              </Badge>
              <span className="text-sm text-muted-foreground">
                {agentStatuses.filter((a) => a.status === "completed").length} / {agentStatuses.length} agents completed
              </span>
            </div>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 lg:grid-cols-2">
        {AGENTS.map((agent, i) => {
          const status = agentStatuses.find((a) => a.agent_type === agent.id);
          const StatusIcon = STATUS_ICONS[status?.status || "pending"];

          return (
            <motion.div
              key={agent.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
            >
              <Card className={`group relative h-full border-border/50 transition-all ${
                status?.status === "completed" ? "border-success/30" :
                status?.status === "running" ? "border-primary/50" :
                status?.status === "failed" ? "border-destructive/30" :
                ""
              }`}>
                <CardContent className="p-6">
                  <div className="mb-4 flex items-start justify-between">
                    <div className={`rounded-xl bg-gradient-to-br ${agent.color} p-3`}>
                      <agent.icon className="h-6 w-6 text-white" />
                    </div>
                    {status && (
                      <div className={`flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ${
                        status.status === "completed" ? "bg-success/10 text-success" :
                        status.status === "running" ? "bg-primary/10 text-primary" :
                        status.status === "failed" ? "bg-destructive/10 text-destructive" :
                        "bg-muted text-muted-foreground"
                      }`}>
                        <StatusIcon className={`h-3 w-3 ${status.status === "running" ? "animate-spin" : ""}`} />
                        {status.status}
                      </div>
                    )}
                  </div>

                  <h3 className="mb-2 text-lg font-semibold">{agent.label}</h3>

                  <AnimatePresence>
                    {status?.output_data && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        className="mt-3 space-y-2"
                      >
                        {status.agent_type === "startup_intelligence" && status.output_data.viability_score && (
                          <div className="flex items-center gap-2 text-sm">
                            <TrendingUp className="h-4 w-4 text-primary" />
                            <span>Viability Score: <strong>{Math.round(status.output_data.viability_score)}/100</strong></span>
                          </div>
                        )}
                        {status.agent_type === "investor_critique" && status.output_data.readiness_score && (
                          <div className="flex items-center gap-2 text-sm">
                            <Shield className="h-4 w-4 text-secondary" />
                            <span>Readiness Score: <strong>{Math.round(status.output_data.readiness_score)}/100</strong></span>
                          </div>
                        )}
                        {status.execution_time_ms && (
                          <p className="text-xs text-muted-foreground">
                            Completed in {(status.execution_time_ms / 1000).toFixed(1)}s
                          </p>
                        )}
                      </motion.div>
                    )}
                  </AnimatePresence>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {currentProject && (
        <Card className="border-border/50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary" />
              Project Summary
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-6 sm:grid-cols-2">
              <div>
                <h4 className="mb-1 text-sm font-medium text-muted-foreground">Problem</h4>
                <p className="text-sm">{currentProject.problem_statement}</p>
              </div>
              <div>
                <h4 className="mb-1 text-sm font-medium text-muted-foreground">Solution</h4>
                <p className="text-sm">{currentProject.solution}</p>
              </div>
              <div>
                <h4 className="mb-1 text-sm font-medium text-muted-foreground">Target Audience</h4>
                <p className="text-sm">{currentProject.target_audience}</p>
              </div>
              <div>
                <h4 className="mb-1 text-sm font-medium text-muted-foreground">Business Model</h4>
                <Badge variant="outline">{currentProject.business_model}</Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </motion.div>
  );
}
