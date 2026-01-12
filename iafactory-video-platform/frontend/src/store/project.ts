/**
 * Project Store - Zustand state management
 */
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import type { Project, Script, Asset, Video } from '@/lib/api';

interface ProjectState {
  // Current project
  currentProject: Project | null;
  currentScript: Script | null;
  assets: Asset[];
  videos: Video[];

  // Pipeline state
  pipelineStatus: 'idle' | 'running' | 'paused' | 'completed' | 'error';
  pipelineProgress: number;
  currentPhase: string | null;

  // UI state
  selectedSceneId: string | null;
  previewMode: 'script' | 'timeline' | 'preview';

  // Actions
  setCurrentProject: (project: Project | null) => void;
  setCurrentScript: (script: Script | null) => void;
  addAsset: (asset: Asset) => void;
  removeAsset: (assetId: string) => void;
  setAssets: (assets: Asset[]) => void;
  addVideo: (video: Video) => void;
  setVideos: (videos: Video[]) => void;

  setPipelineStatus: (status: ProjectState['pipelineStatus']) => void;
  setPipelineProgress: (progress: number) => void;
  setCurrentPhase: (phase: string | null) => void;

  setSelectedSceneId: (sceneId: string | null) => void;
  setPreviewMode: (mode: ProjectState['previewMode']) => void;

  reset: () => void;
}

const initialState = {
  currentProject: null,
  currentScript: null,
  assets: [],
  videos: [],
  pipelineStatus: 'idle' as const,
  pipelineProgress: 0,
  currentPhase: null,
  selectedSceneId: null,
  previewMode: 'script' as const,
};

export const useProjectStore = create<ProjectState>()(
  devtools(
    persist(
      (set) => ({
        ...initialState,

        setCurrentProject: (project) =>
          set({ currentProject: project }, false, 'setCurrentProject'),

        setCurrentScript: (script) =>
          set({ currentScript: script }, false, 'setCurrentScript'),

        addAsset: (asset) =>
          set(
            (state) => ({ assets: [...state.assets, asset] }),
            false,
            'addAsset'
          ),

        removeAsset: (assetId) =>
          set(
            (state) => ({
              assets: state.assets.filter((a) => a.id !== assetId),
            }),
            false,
            'removeAsset'
          ),

        setAssets: (assets) => set({ assets }, false, 'setAssets'),

        addVideo: (video) =>
          set(
            (state) => ({ videos: [...state.videos, video] }),
            false,
            'addVideo'
          ),

        setVideos: (videos) => set({ videos }, false, 'setVideos'),

        setPipelineStatus: (pipelineStatus) =>
          set({ pipelineStatus }, false, 'setPipelineStatus'),

        setPipelineProgress: (pipelineProgress) =>
          set({ pipelineProgress }, false, 'setPipelineProgress'),

        setCurrentPhase: (currentPhase) =>
          set({ currentPhase }, false, 'setCurrentPhase'),

        setSelectedSceneId: (selectedSceneId) =>
          set({ selectedSceneId }, false, 'setSelectedSceneId'),

        setPreviewMode: (previewMode) =>
          set({ previewMode }, false, 'setPreviewMode'),

        reset: () => set(initialState, false, 'reset'),
      }),
      {
        name: 'iafactory-video-project',
        partialize: (state) => ({
          currentProject: state.currentProject,
          previewMode: state.previewMode,
        }),
      }
    ),
    { name: 'ProjectStore' }
  )
);

// Selectors
export const useCurrentProject = () =>
  useProjectStore((state) => state.currentProject);

export const useCurrentScript = () =>
  useProjectStore((state) => state.currentScript);

export const usePipelineStatus = () =>
  useProjectStore((state) => ({
    status: state.pipelineStatus,
    progress: state.pipelineProgress,
    phase: state.currentPhase,
  }));

export const useAssets = () => useProjectStore((state) => state.assets);

export const useVideos = () => useProjectStore((state) => state.videos);
