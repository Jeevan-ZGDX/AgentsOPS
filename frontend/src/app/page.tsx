"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Header } from "@/components/layout/header";
import {
  Bot,
  Brain,
  ChartBar,
  FileText,
  Lightbulb,
  Shield,
  TrendingUp,
  Users,
  ArrowRight,
  CheckCircle,
  Sparkles,
} from "lucide-react";

const fadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
};

const stagger = {
  animate: {
    transition: { staggerChildren: 0.1 },
  },
};

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      <Header />

      <section className="relative overflow-hidden px-4 pb-20 pt-24 sm:px-6 sm:pb-28 sm:pt-32 lg:px-8">
        <div className="absolute inset-0 -z-10">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary/20 via-transparent to-transparent" />
          <div className="absolute left-1/2 top-0 h-px w-1/2 bg-gradient-to-r from-transparent via-primary to-transparent" />
        </div>

        <motion.div
          initial="initial"
          animate="animate"
          variants={stagger}
          className="mx-auto max-w-4xl text-center"
        >
          <motion.div variants={fadeIn} className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-sm text-primary">
            <Sparkles className="h-4 w-4" />
            <span>AI-Powered Startup Intelligence</span>
          </motion.div>

          <motion.h1 variants={fadeIn} className="text-4xl font-bold tracking-tight sm:text-6xl lg:text-7xl">
            Your AI Startup
            <br />
            <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
              Advisory Board
            </span>
          </motion.h1>

          <motion.p variants={fadeIn} className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground sm:text-xl">
            Transform your startup idea into an investor-ready opportunity. AgentOps deploys
            collaborative AI agents for market intelligence, validation, strategy, and pitch generation.
          </motion.p>

          <motion.div variants={fadeIn} className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link href="/auth/register">
              <Button size="xl" className="gap-2 text-base">
                Start Free <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link href="/auth/login">
              <Button variant="outline" size="xl" className="text-base">
                Watch Demo
              </Button>
            </Link>
          </motion.div>

          <motion.div variants={fadeIn} className="mt-8 flex items-center justify-center gap-6 text-sm text-muted-foreground">
            <span className="flex items-center gap-1"><CheckCircle className="h-4 w-4 text-success" /> No credit card</span>
            <span className="flex items-center gap-1"><CheckCircle className="h-4 w-4 text-success" /> Free tier</span>
            <span className="flex items-center gap-1"><CheckCircle className="h-4 w-4 text-success" /> 5 min setup</span>
          </motion.div>
        </motion.div>
      </section>

      <section className="border-t border-border/50 px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center"
          >
            <h2 className="text-3xl font-bold sm:text-4xl">
              From Idea to Investor-Ready in Minutes
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Four specialized AI agents work together to analyze, validate, and prepare your startup.
            </p>
          </motion.div>

          <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {[
              {
                icon: Brain,
                title: "Startup Intelligence",
                desc: "Validates your idea, researches markets, discovers competitors, and generates SWOT analysis.",
                color: "from-blue-500 to-blue-600",
              },
              {
                icon: Lightbulb,
                title: "Business Strategy",
                desc: "Creates business models, pricing strategies, revenue plans, and go-to-market strategies.",
                color: "from-violet-500 to-violet-600",
              },
              {
                icon: Shield,
                title: "Investor Critique",
                desc: "Acts as a VC partner to evaluate risks, assess readiness, and identify red flags.",
                color: "from-emerald-500 to-emerald-600",
              },
              {
                icon: TrendingUp,
                title: "Pitch Intelligence",
                desc: "Crafts executive summaries, pitch narratives, slide decks, and investor messaging.",
                color: "from-amber-500 to-amber-600",
              },
            ].map((feature, i) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
              >
                <Card className="group relative h-full overflow-hidden border-border/50 transition-all hover:border-primary/50 hover:shadow-xl hover:shadow-primary/5">
                  <CardContent className="p-6">
                    <div className={`mb-4 inline-flex rounded-xl bg-gradient-to-br ${feature.color} p-3`}>
                      <feature.icon className="h-6 w-6 text-white" />
                    </div>
                    <h3 className="mb-2 text-lg font-semibold">{feature.title}</h3>
                    <p className="text-sm text-muted-foreground">{feature.desc}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="border-t border-border/50 px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center"
          >
            <h2 className="text-3xl font-bold sm:text-4xl">How It Works</h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Three simple steps to transform your startup idea.
            </p>
          </motion.div>

          <div className="mt-16 grid gap-8 md:grid-cols-3">
            {[
              {
                step: "01",
                title: "Submit Your Idea",
                desc: "Enter your startup name, problem, solution, and target market. Takes 2 minutes.",
              },
              {
                step: "02",
                title: "AI Agent Analysis",
                desc: "Four collaborative agents analyze, critique, and refine your startup in real-time.",
              },
              {
                step: "03",
                title: "Get Intelligence Reports",
                desc: "Receive investor-grade reports, pitch decks, and actionable recommendations.",
              },
            ].map((item, i) => (
              <motion.div
                key={item.step}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15 }}
                className="text-center"
              >
                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-secondary text-2xl font-bold text-white">
                  {item.step}
                </div>
                <h3 className="mb-2 text-xl font-semibold">{item.title}</h3>
                <p className="text-muted-foreground">{item.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="border-t border-border/50 bg-muted/30 px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center"
          >
            <h2 className="text-3xl font-bold sm:text-4xl">Built for Founders</h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Everything you need to go from idea to investment.
            </p>
          </motion.div>

          <div className="mt-16 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {[
              { icon: ChartBar, title: "Market Intelligence", desc: "Real-time market research and competitive analysis" },
              { icon: Bot, title: "Multi-Agent Collaboration", desc: "AI agents work together like your personal advisory board" },
              { icon: FileText, title: "PDF Reports", desc: "Investor-grade PDFs ready for due diligence" },
              { icon: Users, title: "VC Simulation", desc: "Practice your pitch with AI-powered investor critique" },
              { icon: Brain, title: "SWOT Analysis", desc: "Comprehensive strength, weakness, opportunity, threat analysis" },
              { icon: TrendingUp, title: "Scoring System", desc: "Viability and investor readiness scores for every idea" },
            ].map((item, i) => (
              <motion.div
                key={item.title}
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
                className="flex items-start gap-3 rounded-xl border border-border/50 p-4"
              >
                <div className="mt-1 rounded-lg bg-primary/10 p-2">
                  <item.icon className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <h4 className="font-semibold">{item.title}</h4>
                  <p className="text-sm text-muted-foreground">{item.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="border-t border-border/50 px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="relative overflow-hidden rounded-2xl border border-border/50 bg-gradient-to-br from-primary/10 via-secondary/10 to-transparent p-8 sm:p-12"
          >
            <div className="relative z-10 text-center">
              <h2 className="text-3xl font-bold sm:text-4xl">Ready to Build Your Startup?</h2>
              <p className="mx-auto mt-4 max-w-xl text-lg text-muted-foreground">
                Join thousands of founders using AgentOps to validate, strategize, and pitch their ideas.
              </p>
              <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
                <Link href="/auth/register">
                  <Button size="xl" className="gap-2 text-base">
                    Start Free <ArrowRight className="h-4 w-4" />
                  </Button>
                </Link>
                <Link href="/pricing">
                  <Button variant="outline" size="xl" className="text-base">
                    View Pricing
                  </Button>
                </Link>
              </div>
              <p className="mt-4 text-sm text-muted-foreground">Free tier includes 3 projects. No credit card required.</p>
            </div>
          </motion.div>
        </div>
      </section>

      <footer className="border-t border-border/50 px-4 py-12 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
            <div className="flex items-center gap-2">
              <Bot className="h-5 w-5 text-primary" />
              <span className="font-bold">AgentOps</span>
            </div>
            <p className="text-sm text-muted-foreground">
              &copy; {new Date().getFullYear()} AgentOps. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
