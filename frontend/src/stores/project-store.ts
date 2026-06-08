import { create } from "zustand";
import { api } from "@/lib/api";

interface Project {
  id: number;
  owner_id: number;
  name: string;
  industry: string;
  problem_statement: string;
  solution: string;
  target_audience: string;
  business_model: string;
  country: string;
  status: string;
  viability_score: number | null;
  investor_readiness_score: number | null;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

interface ProjectState {
  projects: Project[];
  currentProject: Project | null;
  isLoading: boolean;
  fetchProjects: (status?: string) => Promise<void>;
  fetchProject: (id: number) => Promise<void>;
  createProject: (data: Partial<Project>) => Promise<Project>;
  deleteProject: (id: number) => Promise<void>;
  setCurrentProject: (project: Project | null) => void;
}

export const useProjectStore = create<ProjectState>()((set, get) => ({
  projects: [],
  currentProject: null,
  isLoading: false,

  fetchProjects: async (status?: string) => {
    set({ isLoading: true });
    try {
      const params = status ? { status } : undefined;
      const data = await api.get<{ items: Project[]; total: number }>("/projects", params);
      set({ projects: data.items, isLoading: false });
    } catch {
      set({ isLoading: false });
    }
  },

  fetchProject: async (id: number) => {
    set({ isLoading: true });
    try {
      const project = await api.get<Project>(`/projects/${id}`);
      set({ currentProject: project, isLoading: false });
    } catch {
      set({ isLoading: false });
    }
  },

  createProject: async (data: Partial<Project>) => {
    const project = await api.post<Project>("/projects", data);
    set((state) => ({ projects: [project, ...state.projects] }));
    return project;
  },

  deleteProject: async (id: number) => {
    await api.delete(`/projects/${id}`);
    set((state) => ({
      projects: state.projects.filter((p) => p.id !== id),
      currentProject: state.currentProject?.id === id ? null : state.currentProject,
    }));
  },

  setCurrentProject: (project) => set({ currentProject: project }),
}));
