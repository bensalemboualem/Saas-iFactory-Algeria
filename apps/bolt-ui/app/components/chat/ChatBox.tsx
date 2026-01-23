import React from 'react';
import { ClientOnly } from 'remix-utils/client-only';
import { classNames } from '~/utils/classNames';
import { PROVIDER_LIST } from '~/utils/constants';
import { ModelSelector } from '~/components/chat/ModelSelector';
import { APIKeyManager } from './APIKeyManager';
import { LOCAL_PROVIDERS } from '~/lib/stores/settings';
import FilePreview from './FilePreview';
import { ScreenshotStateManager } from './ScreenshotStateManager';
import { SendButton } from './SendButton.client';
import { IconButton } from '~/components/ui/IconButton';
import { toast } from 'react-toastify';
import { SpeechRecognitionButton } from '~/components/chat/SpeechRecognition';
import { SupabaseConnection } from './SupabaseConnection';
import { ExpoQrModal } from '~/components/workbench/ExpoQrModal';
import styles from './BaseChat.module.scss';
import type { ProviderInfo } from '~/types/model';
import { ColorSchemeDialog } from '~/components/ui/ColorSchemeDialog';
import type { DesignScheme } from '~/types/design-scheme';
import type { ElementInfo } from '~/components/workbench/Inspector';
import { McpTools } from './MCPTools';
import { NexusToggle } from './NexusToggle';

interface ChatBoxProps {
  isModelSettingsCollapsed: boolean;
  setIsModelSettingsCollapsed: (collapsed: boolean) => void;
  provider: any;
  providerList: any[];
  modelList: any[];
  apiKeys: Record<string, string>;
  isModelLoading: string | undefined;
  onApiKeysChange: (providerName: string, apiKey: string) => void;
  uploadedFiles: File[];
  imageDataList: string[];
  textareaRef: React.RefObject<HTMLTextAreaElement> | undefined;
  input: string;
  handlePaste: (e: React.ClipboardEvent) => void;
  TEXTAREA_MIN_HEIGHT: number;
  TEXTAREA_MAX_HEIGHT: number;
  isStreaming: boolean;
  handleSendMessage: (event: React.UIEvent, messageInput?: string) => void;
  isListening: boolean;
  startListening: () => void;
  stopListening: () => void;
  chatStarted: boolean;
  exportChat?: () => void;
  qrModalOpen: boolean;
  setQrModalOpen: (open: boolean) => void;
  handleFileUpload: () => void;
  setProvider?: ((provider: ProviderInfo) => void) | undefined;
  model?: string | undefined;
  setModel?: ((model: string) => void) | undefined;
  setUploadedFiles?: ((files: File[]) => void) | undefined;
  setImageDataList?: ((dataList: string[]) => void) | undefined;
  handleInputChange?: ((event: React.ChangeEvent<HTMLTextAreaElement>) => void) | undefined;
  handleStop?: (() => void) | undefined;
  enhancingPrompt?: boolean | undefined;
  enhancePrompt?: (() => void) | undefined;
  chatMode?: 'discuss' | 'build';
  setChatMode?: (mode: 'discuss' | 'build') => void;
  designScheme?: DesignScheme;
  setDesignScheme?: (scheme: DesignScheme) => void;
  selectedElement?: ElementInfo | null;
  setSelectedElement?: ((element: ElementInfo | null) => void) | undefined;
  isNexusEnabled?: boolean;
  nexusStatus?: string;
}

export const ChatBox: React.FC<ChatBoxProps> = (props) => {
  // --- TYPEWRITER LOGIC ---
  const [placeholderText, setPlaceholderText] = React.useState('');
  const [isDeleting, setIsDeleting] = React.useState(false);
  const [loopNum, setLoopNum] = React.useState(0);
  const [typingSpeed, setTypingSpeed] = React.useState(100);

  const modeExamples: Record<string, string[]> = {
    chat: [
      "💬 Mode Discussion : Pose-moi n'importe quelle question...",
      "💡 Je suis là pour t'aider sur des sujets généraux.",
      "🧠 Besoin d'un conseil ou d'une explication ?"
    ],
    bolt: [
      "⚡ Mode Création (IDE) : Décris ton application Web...",
      "🛠️ Je vais générer le code et l'interface pour toi.",
      "🎨 'Crée une landing page pour une pizzeria...'"
    ],
    nexus: [
      "🧭 Mode Orchestrateur : Brainstorming avec les agents BMAD...",
      "🤖 Agents : Validation du projet -> Archon (Base de Connaissance)...",
      "🏗️ Workflow : Prompt Finalisé -> Génération Bolt (Site/Apps)."
    ]
  };

  React.useEffect(() => {
    let mode = 'chat';
    if (props.isNexusEnabled) mode = 'nexus';
    else if (props.chatMode === 'build') mode = 'bolt';

    const i = loopNum % modeExamples[mode].length;
    const fullText = modeExamples[mode][i];

    const handleTyping = () => {
      setPlaceholderText(isDeleting
        ? fullText.substring(0, placeholderText.length - 1)
        : fullText.substring(0, placeholderText.length + 1)
      );

      setTypingSpeed(isDeleting ? 30 : 100);

      if (!isDeleting && placeholderText === fullText) {
        setTimeout(() => setIsDeleting(true), 2000); // Wait before deleting
      } else if (isDeleting && placeholderText === '') {
        setIsDeleting(false);
        setLoopNum(loopNum + 1);
      }
    };

    const timer = setTimeout(handleTyping, typingSpeed);
    return () => clearTimeout(timer);
  }, [placeholderText, isDeleting, loopNum, typingSpeed, props.chatMode, props.isNexusEnabled]);

  // --- HANDLERS ---
  const switchToChat = async () => {
    props.setChatMode?.('discuss');
    if (props.isNexusEnabled) {
      const { setNexusMode } = await import('~/lib/modules/nexus/store');
      setNexusMode(false);
    }
  };

  const switchToBolt = async () => {
    props.setChatMode?.('build');
    if (props.isNexusEnabled) {
      const { setNexusMode } = await import('~/lib/modules/nexus/store');
      setNexusMode(false);
    }
  };

  const switchToNexus = async () => {
    props.setChatMode?.('discuss'); // Nexus runs in discuss mode primarily
    if (!props.isNexusEnabled) {
      const { setNexusMode } = await import('~/lib/modules/nexus/store');
      setNexusMode(true);
    }
  };

  return (
    <div
      className={classNames(
        'relative bg-bolt-elements-background-depth-2 backdrop-blur p-3 rounded-lg border border-bolt-elements-borderColor relative w-full max-w-chat mx-auto z-prompt',
      )}
    >
      <svg className={classNames(styles.PromptEffectContainer)}>
        <defs>
          <linearGradient
            id="line-gradient"
            x1="20%"
            y1="0%"
            x2="-14%"
            y2="10%"
            gradientUnits="userSpaceOnUse"
            gradientTransform="rotate(-45)"
          >
            <stop offset="0%" stopColor="#b44aff" stopOpacity="0%"></stop>
            <stop offset="40%" stopColor="#b44aff" stopOpacity="80%"></stop>
            <stop offset="50%" stopColor="#b44aff" stopOpacity="80%"></stop>
            <stop offset="100%" stopColor="#b44aff" stopOpacity="0%"></stop>
          </linearGradient>
          <linearGradient id="shine-gradient">
            <stop offset="0%" stopColor="white" stopOpacity="0%"></stop>
            <stop offset="40%" stopColor="#ffffff" stopOpacity="80%"></stop>
            <stop offset="50%" stopColor="#ffffff" stopOpacity="80%"></stop>
            <stop offset="100%" stopColor="white" stopOpacity="0%"></stop>
          </linearGradient>
        </defs>
        <rect className={classNames(styles.PromptEffectLine)} pathLength="100" strokeLinecap="round"></rect>
        <rect className={classNames(styles.PromptShine)} x="48" y="24" width="70" height="1"></rect>
      </svg>
      <div>
        <ClientOnly>
          {() => (
            <div className={props.isModelSettingsCollapsed ? 'hidden' : ''}>
              <ModelSelector
                key={props.provider?.name + ':' + props.modelList.length}
                model={props.model}
                setModel={props.setModel}
                modelList={props.modelList}
                provider={props.provider}
                setProvider={props.setProvider}
                providerList={props.providerList || (PROVIDER_LIST as ProviderInfo[])}
                apiKeys={props.apiKeys}
                modelLoading={props.isModelLoading}
              />
              {(props.providerList || []).length > 0 &&
                props.provider &&
                !LOCAL_PROVIDERS.includes(props.provider.name) && (
                  <APIKeyManager
                    provider={props.provider}
                    apiKey={props.apiKeys[props.provider.name] || ''}
                    setApiKey={(key) => {
                      props.onApiKeysChange(props.provider.name, key);
                    }}
                  />
                )}
            </div>
          )}
        </ClientOnly>
      </div>
      <FilePreview
        files={props.uploadedFiles}
        imageDataList={props.imageDataList}
        onRemove={(index) => {
          props.setUploadedFiles?.(props.uploadedFiles.filter((_, i) => i !== index));
          props.setImageDataList?.(props.imageDataList.filter((_, i) => i !== index));
        }}
      />
      <ClientOnly>
        {() => (
          <ScreenshotStateManager
            setUploadedFiles={props.setUploadedFiles}
            setImageDataList={props.setImageDataList}
            uploadedFiles={props.uploadedFiles}
            imageDataList={props.imageDataList}
          />
        )}
      </ClientOnly>
      {props.selectedElement && (
        <div className="flex mx-1.5 gap-2 items-center justify-between rounded-lg rounded-b-none border border-b-none border-bolt-elements-borderColor text-bolt-elements-textPrimary flex py-1 px-2.5 font-medium text-xs">
          <div className="flex gap-2 items-center lowercase">
            <code className="bg-accent-500 rounded-4px px-1.5 py-1 mr-0.5 text-white">
              {props?.selectedElement?.tagName}
            </code>
            selected for inspection
          </div>
          <button
            className="bg-transparent text-accent-500 pointer-auto"
            onClick={() => props.setSelectedElement?.(null)}
          >
            Clear
          </button>
        </div>
      )}
      <div
        className={classNames('relative shadow-xs border border-bolt-elements-borderColor backdrop-blur rounded-lg')}
      >
        <textarea
          ref={props.textareaRef}
          data-testid="chat-input"
          className={classNames(
            'w-full pl-4 pt-4 pr-16 outline-none resize-none text-bolt-elements-textPrimary placeholder-bolt-elements-textTertiary bg-transparent text-sm',
            'transition-all duration-200',
            'hover:border-bolt-elements-focus',
          )}
          onDragEnter={(e) => {
            e.preventDefault();
            e.currentTarget.style.border = '2px solid #1488fc';
          }}
          onDragOver={(e) => {
            e.preventDefault();
            e.currentTarget.style.border = '2px solid #1488fc';
          }}
          onDragLeave={(e) => {
            e.preventDefault();
            e.currentTarget.style.border = '1px solid var(--bolt-elements-borderColor)';
          }}
          onDrop={(e) => {
            e.preventDefault();
            e.currentTarget.style.border = '1px solid var(--bolt-elements-borderColor)';

            const files = Array.from(e.dataTransfer.files);
            files.forEach((file) => {
              if (file.type.startsWith('image/')) {
                const reader = new FileReader();

                reader.onload = (e) => {
                  const base64Image = e.target?.result as string;
                  props.setUploadedFiles?.([...props.uploadedFiles, file]);
                  props.setImageDataList?.([...props.imageDataList, base64Image]);
                };
                reader.readAsDataURL(file);
              }
            });
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter') {
              if (event.shiftKey) {
                return;
              }

              event.preventDefault();

              if (props.isStreaming) {
                props.handleStop?.();
                return;
              }

              // ignore if using input method engine
              if (event.nativeEvent.isComposing) {
                return;
              }

              props.handleSendMessage?.(event);
            }
          }}
          value={props.input}
          onChange={(event) => {
            props.handleInputChange?.(event);
          }}
          onPaste={props.handlePaste}
          style={{
            minHeight: props.TEXTAREA_MIN_HEIGHT,
            maxHeight: props.TEXTAREA_MAX_HEIGHT,
          }}
          placeholder={placeholderText}
          translate="no"
        />
        <ClientOnly>
          {() => (
            <SendButton
              show={props.input.length > 0 || props.isStreaming || props.uploadedFiles.length > 0}
              isStreaming={props.isStreaming}
              disabled={!props.providerList || props.providerList.length === 0}
              onClick={(event) => {
                if (props.isStreaming) {
                  props.handleStop?.();
                  return;
                }

                if (props.input.length > 0 || props.uploadedFiles.length > 0) {
                  props.handleSendMessage?.(event);
                }
              }}
            />
          )}
        </ClientOnly>
        <div className="flex justify-between items-center text-sm p-4 pt-2">

          {/* --- PRO MODE SWITCHER --- */}
          <div className="flex items-center gap-1 w-full md:w-auto">
            <div className="flex bg-bolt-elements-background-depth-3 rounded-lg p-1 border border-bolt-elements-borderColor w-full md:w-auto">
              <button
                onClick={switchToChat}
                className={classNames(
                  'flex-1 md:flex-none px-4 py-1.5 rounded-md text-xs font-semibold transition-all flex justify-center items-center gap-2',
                  props.chatMode === 'discuss' && !props.isNexusEnabled
                    ? 'bg-bolt-elements-item-backgroundAccent text-bolt-elements-item-contentAccent shadow-sm'
                    : 'text-bolt-elements-textSecondary hover:text-bolt-elements-textPrimary'
                )}
              >
                <div className="i-ph:chat-circle-dots text-sm" />
                Chat
              </button>

              <button
                onClick={switchToBolt}
                className={classNames(
                  'flex-1 md:flex-none px-4 py-1.5 rounded-md text-xs font-semibold transition-all flex justify-center items-center gap-2',
                  props.chatMode === 'build' && !props.isNexusEnabled
                    ? 'bg-bolt-elements-item-backgroundAccent text-bolt-elements-item-contentAccent shadow-sm'
                    : 'text-bolt-elements-textSecondary hover:text-bolt-elements-textPrimary'
                )}
              >
                <div className="i-ph:lightning text-sm" />
                Bolt
              </button>

              <button
                onClick={switchToNexus}
                className={classNames(
                  'flex-1 md:flex-none px-4 py-1.5 rounded-md text-xs font-semibold transition-all flex justify-center items-center gap-2',
                  props.isNexusEnabled
                    ? 'bg-green-500 text-white shadow-sm ring-1 ring-green-600'
                    : 'text-bolt-elements-textSecondary hover:text-bolt-elements-textPrimary'
                )}
              >
                <div className="i-ph:compass text-sm" />
                Nexus
              </button>
            </div>

            <div className="w-px h-6 bg-bolt-elements-borderColor mx-2 hidden md:block" />

            <div className="hidden md:flex items-center gap-1">
              <ColorSchemeDialog designScheme={props.designScheme} setDesignScheme={props.setDesignScheme} />
              <McpTools />
              <IconButton title="Upload file" className="transition-all" onClick={() => props.handleFileUpload()}>
                <div className="i-ph:paperclip text-xl"></div>
              </IconButton>
              <IconButton
                title="Enhance prompt"
                disabled={props.input.length === 0 || props.enhancingPrompt}
                className={classNames('transition-all', props.enhancingPrompt ? 'opacity-100' : '')}
                onClick={() => {
                  props.enhancePrompt?.();
                  toast.success('Prompt enhanced!');
                }}
              >
                {props.enhancingPrompt ? (
                  <div className="i-svg-spinners:90-ring-with-bg text-bolt-elements-loader-progress text-xl animate-spin"></div>
                ) : (
                  <div className="i-bolt:stars text-xl"></div>
                )}
              </IconButton>
            </div>
          </div>

          {props.input.length > 3 ? (
            <div className="hidden md:block text-xs text-bolt-elements-textTertiary">
              Use <kbd className="kdb px-1.5 py-0.5 rounded bg-bolt-elements-background-depth-2">Shift</kbd> +{' '}
              <kbd className="kdb px-1.5 py-0.5 rounded bg-bolt-elements-background-depth-2">Return</kbd> a new line
            </div>
          ) : null}
          <SupabaseConnection />
          <ExpoQrModal open={props.qrModalOpen} onClose={() => props.setQrModalOpen(false)} />

        </div>
      </div>
    </div>
  );
};
