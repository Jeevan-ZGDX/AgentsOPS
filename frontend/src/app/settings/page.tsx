"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useAuthStore } from "@/stores/auth-store";
import { User, Shield, Key, Bell, CreditCard } from "lucide-react";
import { toast } from "sonner";

const TABS = [
  { id: "profile", label: "Profile", icon: User },
  { id: "security", label: "Security", icon: Shield },
  { id: "api-keys", label: "API Keys", icon: Key },
  { id: "billing", label: "Billing", icon: CreditCard },
  { id: "notifications", label: "Notifications", icon: Bell },
];

export default function SettingsPage() {
  const { user } = useAuthStore();
  const [activeTab, setActiveTab] = useState("profile");

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground">Manage your account and preferences.</p>
      </div>

      <div className="flex gap-2 overflow-x-auto pb-2">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 whitespace-nowrap rounded-lg px-4 py-2 text-sm font-medium transition-all ${
              activeTab === tab.id
                ? "bg-primary text-white"
                : "text-muted-foreground hover:bg-muted hover:text-foreground"
            }`}
          >
            <tab.icon className="h-4 w-4" />
            {tab.label}
          </button>
        ))}
      </div>

      <Card className="border-border/50">
        {activeTab === "profile" && (
          <>
            <CardHeader>
              <CardTitle>Profile</CardTitle>
              <CardDescription>Update your personal information.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 sm:grid-cols-2">
                <div>
                  <label className="mb-1.5 block text-sm font-medium">Full Name</label>
                  <Input defaultValue={user?.full_name || ""} placeholder="Your name" />
                </div>
                <div>
                  <label className="mb-1.5 block text-sm font-medium">Email</label>
                  <Input defaultValue={user?.email || ""} disabled />
                </div>
              </div>
              <Button>Save Changes</Button>
            </CardContent>
          </>
        )}

        {activeTab === "security" && (
          <>
            <CardHeader>
              <CardTitle>Security</CardTitle>
              <CardDescription>Manage your password and security settings.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 sm:grid-cols-2">
                <div>
                  <label className="mb-1.5 block text-sm font-medium">Current Password</label>
                  <Input type="password" />
                </div>
                <div>
                  <label className="mb-1.5 block text-sm font-medium">New Password</label>
                  <Input type="password" />
                </div>
              </div>
              <Button>Update Password</Button>
            </CardContent>
          </>
        )}

        {activeTab === "api-keys" && (
          <>
            <CardHeader>
              <CardTitle>API Keys</CardTitle>
              <CardDescription>Manage your API keys for programmatic access.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between rounded-lg border border-border/50 p-4">
                <div>
                  <p className="text-sm font-medium">No API keys yet</p>
                  <p className="text-xs text-muted-foreground">Create an API key to access AgentOps programmatically.</p>
                </div>
                <Button size="sm">Create Key</Button>
              </div>
            </CardContent>
          </>
        )}

        {activeTab === "billing" && (
          <>
            <CardHeader>
              <CardTitle>Billing</CardTitle>
              <CardDescription>Manage your subscription and billing information.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="rounded-lg border border-border/50 p-6 text-center">
                <p className="mb-2 text-lg font-semibold">Free Plan</p>
                <p className="mb-4 text-sm text-muted-foreground">3 projects &middot; 1 agent per project &middot; Basic reports</p>
                <Button variant="outline">Upgrade to Pro</Button>
              </div>
            </CardContent>
          </>
        )}

        {activeTab === "notifications" && (
          <>
            <CardHeader>
              <CardTitle>Notifications</CardTitle>
              <CardDescription>Configure your notification preferences.</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">Notification settings coming soon.</p>
            </CardContent>
          </>
        )}
      </Card>
    </motion.div>
  );
}
