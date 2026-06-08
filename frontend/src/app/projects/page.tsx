"use client";

import { useEffect } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useProjectStore } from "@/stores/project-store";
import { Plus, FolderKanban, TrendingUp, Shield, ExternalLink, Trash2 } from "lucide-react";
import { formatDate, formatScore } from "@/lib/utils";
import { toast } from "sonner";

export default function ProjectsPage() {
  const { projects, isLoading, fetchProjects, deleteProject } = useProjectStore();

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleDelete = async (id: number, name: string) => {
    if (confirm(`Delete "${name}"? This action cannot be undone.`)) {
      try {
        await deleteProject(id);
        toast.success("Project deleted");
      } catch {
        toast.error("Failed to delete project");
      }
    }
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Projects</h1>
          <p className="text-muted-foreground">Manage your startup ideas</p>
        </div>
        <Link href="/projects/new">
          <Button className="gap-2">
            <Plus className="h-4 w-4" /> New Project
          </Button>
        </Link>
      </div>

      {isLoading ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-48 rounded-xl" />
          ))}
        </div>
      ) : projects.length === 0 ? (
        <Card className="border-border/50">
          <CardContent className="flex flex-col items-center gap-4 py-16 text-center">
            <FolderKanban className="h-16 w-16 text-muted-foreground/30" />
            <h3 className="text-xl font-semibold">No projects yet</h3>
            <p className="text-muted-foreground">Create your first startup project to get AI-powered intelligence.</p>
            <Link href="/projects/new">
              <Button className="gap-2">
                <Plus className="h-4 w-4" /> Create Your First Project
              </Button>
            </Link>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {projects.map((project, i) => (
            <motion.div
              key={project.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
            >
              <Link href={`/workspace?project=${project.id}`}>
                <Card className="group relative h-full border-border/50 transition-all hover:border-primary/50 hover:shadow-xl hover:shadow-primary/5">
                  <CardContent className="p-6">
                    <div className="mb-4 flex items-start justify-between">
                      <div className="rounded-xl bg-gradient-to-br from-primary/10 to-secondary/10 p-3">
                        <FolderKanban className="h-6 w-6 text-primary" />
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
                    </div>

                    <h3 className="mb-1 text-lg font-semibold">{project.name}</h3>
                    <p className="mb-4 text-sm text-muted-foreground">{project.industry}</p>

                    <div className="mb-4 flex gap-4 text-sm">
                      {project.viability_score && (
                        <div className="flex items-center gap-1">
                          <TrendingUp className="h-3.5 w-3.5 text-primary" />
                          <span>{formatScore(project.viability_score)}</span>
                        </div>
                      )}
                      {project.investor_readiness_score && (
                        <div className="flex items-center gap-1">
                          <Shield className="h-3.5 w-3.5 text-secondary" />
                          <span>{formatScore(project.investor_readiness_score)}</span>
                        </div>
                      )}
                    </div>

                    <div className="flex items-center justify-between text-xs text-muted-foreground">
                      <span>{formatDate(project.created_at)}</span>
                      <ExternalLink className="h-3.5 w-3.5 opacity-0 transition-opacity group-hover:opacity-100" />
                    </div>
                  </CardContent>
                </Card>
              </Link>
            </motion.div>
          ))}
        </div>
      )}
    </motion.div>
  );
}
