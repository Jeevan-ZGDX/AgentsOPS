"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { api } from "@/lib/api";
import { FileText, Download, File, FileSpreadsheet, Eye, Sparkles } from "lucide-react";
import { formatDate } from "@/lib/utils";
import { toast } from "sonner";

interface Report {
  id: number;
  project_id: number;
  report_type: string;
  format: string;
  status: string;
  title: string;
  file_path: string | null;
  created_at: string;
}

export default function ReportsPage() {
  const searchParams = useSearchParams();
  const projectId = searchParams.get("project");
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    if (projectId) {
      fetchReports(Number(projectId));
    } else {
      setLoading(false);
    }
  }, [projectId]);

  const fetchReports = async (id: number) => {
    try {
      const data = await api.get<{ items: Report[] }>(`/reports/${id}`);
      setReports(data.items);
    } catch {
      // No reports yet
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    if (!projectId) return;
    setGenerating(true);
    try {
      await api.post("/reports/generate", { project_id: Number(projectId), report_type: "unified", formats: ["pdf"] });
      toast.success("Report generation started");
      setTimeout(() => fetchReports(Number(projectId)), 3000);
    } catch (err: any) {
      toast.error(err.message || "Failed to generate report");
    } finally {
      setGenerating(false);
    }
  };

  const handleExport = async (format: string) => {
    if (!projectId) return;
    try {
      const data = await api.post<{ report_id: number }>("/reports/export", {
        project_id: Number(projectId),
        format,
      });
      toast.success(`${format.toUpperCase()} export started`);
    } catch (err: any) {
      toast.error(err.message || `Failed to export ${format}`);
    }
  };

  const getReportIcon = (type: string) => {
    switch (type) {
      case "startup": return Eye;
      case "business_strategy": return File;
      case "investor": return FileSpreadsheet;
      case "pitch": return Sparkles;
      default: return FileText;
    }
  };

  if (!projectId) {
    return (
      <div className="flex flex-col items-center justify-center py-32 text-center">
        <FileText className="mb-4 h-16 w-16 text-muted-foreground/30" />
        <h2 className="mb-2 text-2xl font-bold">No Project Selected</h2>
        <p className="text-muted-foreground">Select a project to view or generate reports.</p>
      </div>
    );
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Reports</h1>
          <p className="text-muted-foreground">View and export intelligence reports for project #{projectId}</p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline" className="gap-2" onClick={() => handleExport("pdf")}>
            <Download className="h-4 w-4" /> Export PDF
          </Button>
          <Button variant="outline" className="gap-2" onClick={() => handleExport("ppt")}>
            <File className="h-4 w-4" /> Export PPT
          </Button>
          <Button className="gap-2" onClick={handleGenerate} disabled={generating}>
            <Sparkles className="h-4 w-4" /> Generate Report
          </Button>
        </div>
      </div>

      {loading ? (
        <div className="space-y-4">
          {[1, 2, 3].map((i) => <Skeleton key={i} className="h-24 rounded-xl" />)}
        </div>
      ) : reports.length === 0 ? (
        <Card className="border-border/50">
          <CardContent className="flex flex-col items-center gap-4 py-16 text-center">
            <FileText className="h-16 w-16 text-muted-foreground/30" />
            <h3 className="text-xl font-semibold">No reports yet</h3>
            <p className="text-muted-foreground">Run the agent workflow first, then generate reports.</p>
            <Button className="gap-2" onClick={handleGenerate} disabled={generating}>
              <Sparkles className="h-4 w-4" /> Generate Report
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {reports.map((report) => {
            const Icon = getReportIcon(report.report_type);
            return (
              <Card key={report.id} className="border-border/50 transition-all hover:border-primary/50">
                <CardContent className="flex items-center justify-between p-4">
                  <div className="flex items-center gap-4">
                    <div className="rounded-lg bg-primary/10 p-2.5">
                      <Icon className="h-5 w-5 text-primary" />
                    </div>
                    <div>
                      <p className="font-medium">{report.title}</p>
                      <div className="mt-1 flex items-center gap-3 text-xs text-muted-foreground">
                        <Badge variant="outline" className="text-xs">{report.report_type}</Badge>
                        <Badge variant="outline" className="text-xs uppercase">{report.format}</Badge>
                        <span>{formatDate(report.created_at)}</span>
                      </div>
                    </div>
                  </div>
                  <Badge
                    variant={
                      report.status === "completed" ? "success" :
                      report.status === "generating" ? "warning" :
                      "destructive"
                    }
                  >
                    {report.status}
                  </Badge>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </motion.div>
  );
}
