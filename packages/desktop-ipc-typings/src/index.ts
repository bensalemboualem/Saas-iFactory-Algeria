// Desktop IPC Typings for IAFactory
// Types for Electron IPC communication

export interface IpcMainEvent {
  sender: unknown;
  reply: (channel: string, ...args: unknown[]) => void;
}

export interface IpcRendererEvent {
  sender: unknown;
  senderId: number;
}

export interface DesktopIpcChannels {
  // File operations
  'file:open': { path: string };
  'file:save': { path: string; content: string };
  'file:read': { path: string };
  
  // App operations
  'app:minimize': void;
  'app:maximize': void;
  'app:close': void;
  'app:ready': void;
}

export type IpcChannel = keyof DesktopIpcChannels;

export default DesktopIpcChannels;
