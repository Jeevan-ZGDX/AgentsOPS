"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { useProjectStore } from "@/stores/project-store";
import { Bot, ArrowRight, Sparkles } from "lucide-react";
import { toast } from "sonner";

const INDUSTRIES = [
  "AI/ML", "FinTech", "HealthTech", "EdTech", "SaaS", "E-Commerce",
  "CleanTech", "BioTech", "PropTech", "LegalTech", "AgriTech", "Gaming",
  "Cybersecurity", "DevTools", "Marketplace", "Social", "Other",
];

const BUSINESS_MODELS = [
  { value: "b2b_saas", label: "B2B SaaS" },
  { value: "b2c_saas", label: "B2C SaaS" },
  { value: "marketplace", label: "Marketplace" },
  { value: "e_commerce", label: "E-Commerce" },
  { value: "subscription", label: "Subscription" },
  { value: "freemium", label: "Freemium" },
  { value: "advertising", label: "Advertising" },
  { value: "licensing", label: "Licensing" },
  { value: "consulting", label: "Consulting" },
  { value: "hybrid", label: "Hybrid" },
];

export default function NewProjectPage() {
  const router = useRouter();
  const { createProject } = useProjectStore();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    name: "",
    industry: "",
    problem_statement: "",
    solution: "",
    target_audience: "",
    business_model: "",
    country: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.industry || !form.business_model) {
      toast.error("Please select industry and business model");
      return;
    }
    setLoading(true);
    try {
      const project = await createProject(form);
      toast.success("Project created!");
      router.push(`/workspace?project=${project.id}`);
    } catch (err: any) {
      toast.error(err.message || "Failed to create project");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mx-auto max-w-3xl space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">New Project</h1>
        <p className="text-muted-foreground">Describe your startup idea and let AI analyze it.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <Card className="border-border/50">
          <CardHeader>
            <CardTitle>Startup Details</CardTitle>
            <CardDescription>Provide information about your startup idea.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="mb-1.5 block text-sm font-medium">Startup Name *</label>
              <Input
                placeholder="e.g., FarmAI Assistant"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
              />
            </div>

            <div>
              <label className="mb-1.5 block text-sm font-medium">Industry *</label>
              <div className="flex flex-wrap gap-2">
                {INDUSTRIES.map((ind) => (
                  <button
                    key={ind}
                    type="button"
                    onClick={() => setForm({ ...form, industry: ind })}
                    className={`rounded-lg border px-3 py-1.5 text-sm transition-all ${
                      form.industry === ind
                        ? "border-primary bg-primary/10 text-primary"
                        : "border-border hover:border-primary/50"
                    }`}
                  >
                    {ind}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="mb-1.5 block text-sm font-medium">Problem Statement *</label>
              <Textarea
                placeholder="What problem does your startup solve?"
                className="min-h-[100px]"
                value={form.problem_statement}
                onChange={(e) => setForm({ ...form, problem_statement: e.target.value })}
                required
              />
            </div>

            <div>
              <label className="mb-1.5 block text-sm font-medium">Solution *</label>
              <Textarea
                placeholder="How does your product solve this problem?"
                className="min-h-[100px]"
                value={form.solution}
                onChange={(e) => setForm({ ...form, solution: e.target.value })}
                required
              />
            </div>

            <div>
              <label className="mb-1.5 block text-sm font-medium">Target Audience *</label>
              <Input
                placeholder="e.g., Small farmers in developing countries"
                value={form.target_audience}
                onChange={(e) => setForm({ ...form, target_audience: e.target.value })}
                required
              />
            </div>

            <div>
              <label className="mb-1.5 block text-sm font-medium">Business Model *</label>
              <div className="flex flex-wrap gap-2">
                {BUSINESS_MODELS.map((bm) => (
                  <button
                    key={bm.value}
                    type="button"
                    onClick={() => setForm({ ...form, business_model: bm.value })}
                    className={`rounded-lg border px-3 py-1.5 text-sm transition-all ${
                      form.business_model === bm.value
                        ? "border-primary bg-primary/10 text-primary"
                        : "border-border hover:border-primary/50"
                    }`}
                  >
                    {bm.label}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="mb-1.5 block text-sm font-medium">Country *</label>
              <Input
                placeholder="e.g., India"
                value={form.country}
                onChange={(e) => setForm({ ...form, country: e.target.value })}
                required
              />
            </div>
          </CardContent>
        </Card>

        <div className="flex justify-end gap-3">
          <Button type="button" variant="outline" onClick={() => router.back()}>
            Cancel
          </Button>
          <Button type="submit" size="lg" className="gap-2" disabled={loading}>
            {loading ? (
              "Creating..."
            ) : (
              <>
                <Sparkles className="h-4 w-4" /> Analyze with AI <ArrowRight className="h-4 w-4" />
              </>
            )}
          </Button>
        </div>
      </form>
    </motion.div>
  );
}
