"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { api } from "@/lib/api";
import { useProjectStore } from "@/stores/project-store";
import {
  Plus,
  FolderKanban,
  Bot,
  FileText,
  TrendingUp,
  Shield,
  ArrowRight,
  BarChart3,
} from "lucide-react";

interface Overview {
  total_projects: number;
  active_projects: number;
  completed_projects: number;
  total_reports: number;
  avg_viability_score: number | null;
  avg_investor_readiness: number | null;
  recent_projects: any[];
}

export default function DashboardPage() {
  const [overview, setOverview] = useState<Overview | null>(null);
  const [loading, setLoading] = useState(true);
  const { fetchProjects, projects } = useProjectStore();

  useEffect(() => {
    fetchProjects();
    api.get<Overview>("/dashboard/overview")
      .then(setOverview)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-8 w-48" />
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[1, 2, 3, 4].map((i) => <Skeleton key={i} className="h-32 rounded-xl" />)}
        </div>
      </div>
    );
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground">Your startup intelligence overview</p>
        </div>
        <Link href="/projects/new">
          <Button className="gap-2">
            <Plus className="h-4 w-4" /> New Project
          </Button>
        </Link>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[
          { label: "Total Projects", value: overview?.total_projects || 0, icon: FolderKanban, color: "from-blue-500 to-blue-600" },
          { label: "Active", value: overview?.active_projects || 0, icon: Bot, color: "from-violet-500 to-violet-600" },
          { label: "Reports Generated", value: overview?.total_reports || 0, icon: FileText, color: "from-emerald-500 to-emerald-600" },
          { label: "Completed", value: overview?.completed_projects || 0, icon: BarChart3, color: "from-amber-500 to-amber-600" },
        ].map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
          >
            <Card className="border-border/50 transition-all hover:border-primary/50">
              <CardContent className="flex items-center gap-4 p-6">
                <div className={`rounded-xl bg-gradient-to-br ${stat.color} p-3`}>
                  <stat.icon className="h-6 w-6 text-white" />
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">{stat.label}</p>
                  <p className="text-2xl font-bold">{stat.value}</p>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card className="border-border/50">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Scores</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <div className="mb-2 flex items-center justify-between">
                  <span className="flex items-center gap-2 text-sm">
                    <TrendingUp className="h-4 w-4 text-primary" /> Viability Score
                  </span>
                  <span className="text-sm font-bold">
                    {overview?.avg_viability_score ? `${Math.round(overview.avg_viability_score)}/100` : "N/A"}
                  </span>
                </div>
                <div className="h-2 rounded-full bg-muted">
                  <div
                    className="h-2 rounded-full bg-gradient-to-r from-primary to-secondary transition-all"
                    style={{ width: `${overview?.avg_viability_score || 0}%` }}
                  />
                </div>
              </div>
              <div>
                <div className="mb-2 flex items-center justify-between">
                  <span className="flex items-center gap-2 text-sm">
                    <Shield className="h-4 w-4 text-secondary" /> Investor Readiness
                  </span>
                  <span className="text-sm font-bold">
                    {overview?.avg_investor_readiness ? `${Math.round(overview.avg_investor_readiness)}/100` : "N/A"}
                  </span>
                </div>
                <div className="h-2 rounded-full bg-muted">
                  <div
                    className="h-2 rounded-full bg-gradient-to-r from-secondary to-primary transition-all"
                    style={{ width: `${overview?.avg_investor_readiness || 0}%` }}
                  />
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border/50">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Recent Projects</CardTitle>
            <Link href="/projects">
              <Button variant="ghost" size="sm" className="gap-1">
                View All <ArrowRight className="h-3 w-3" />
              </Button>
            </Link>
          </CardHeader>
          <CardContent>
            {projects.length === 0 ? (
              <div className="flex flex-col items-center gap-3 py-8 text-center">
                <FolderKanban className="h-12 w-12 text-muted-foreground/50" />
                <p className="text-sm text-muted-foreground">No projects yet</p>
                <Link href="/projects/new">
                  <Button size="sm" className="gap-2">
                    <Plus className="h-4 w-4" /> Create Your First Project
                  </Button>
                </Link>
              </div>
            ) : (
              <div className="space-y-3">
                {projects.slice(0, 5).map((project) => (
                  <Link
                    key={project.id}
                    href={`/projects/${project.id}`}
                    className="flex items-center justify-between rounded-lg border border-border/50 p-3 transition-all hover:border-primary/50 hover:bg-muted/50"
                  >
                    <div>
                      <p className="font-medium">{project.name}</p>
                      <p className="text-xs text-muted-foreground">{project.industry}</p>
                    </div>
                    <Badge
                      variant={
                        project.status === "completed" ? "success" :
                        project.status === "in_progress" ? "warning" :
                        "secondary"
                      }
                    >
                      {project.status}
                    </Badge>
                  </Link>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </motion.div>
  );
}
