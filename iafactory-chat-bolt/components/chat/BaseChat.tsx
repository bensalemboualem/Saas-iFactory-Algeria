/*
 * @ts-nocheck
 * Preventing TS checks with files presented in the video for a better presentation.
 */
import type { JSONValue, Message } from 'ai';
import React, { type RefCallback, useEffect, useState } from 'react';
import { ClientOnly } from 'remix-utils/client-only';
import { Menu } from '~/components/sidebar/Menu.client';
import { Workbench } from '~/components/workbench/Workbench.client';
import { classNames } from '~/utils/classNames';
import { PROVIDER_LIST } from '~/utils/constants';
import { Messages } from './Messages.client';
import { getApiKeysFromCookies } from './APIKeyManager';
import Cookies from 'js-cookie';
import * as Tooltip from '@radix-ui/react-tooltip';
import styles from './BaseChat.module.scss';
import { ImportButtons } from '~/components/chat/chatExportAndImport/ImportButtons';
import { ExamplePrompts } from '~/components/chat/ExamplePrompts';
import GitCloneButton from './GitCloneButton';
import type { ProviderInfo } from '~/types/model';
import StarterTemplates from './StarterTemplates';
import type { ActionAlert, SupabaseAlert, DeployAlert, LlmErrorAlertType } from '~/types/actions';
import DeployChatAlert from '~/components/deploy/DeployAlert';
import ChatAlert from './ChatAlert';
import type { ModelInfo } from '~/lib/modules/llm/types';
import ProgressCompilation from './ProgressCompilation';
import type { ProgressAnnotation } from '~/types/context';
import { SupabaseChatAlert } from '~/components/chat/SupabaseAlert';
import { expoUrlAtom } from '~/lib/stores/qrCodeStore';
import { useStore } from '@nanostores/react';
import { StickToBottom, useStickToBottomContext } from '~/lib/hooks';
import { ChatBox } from './ChatBox';
import type { DesignScheme } from '~/types/design-scheme';
import type { ElementInfo } from '~/components/workbench/Inspector';
import LlmErrorAlert from './LLMApiAlert';
import { nexusModeEnabled, nexusConnectionStatus } from '~/lib/modules/nexus/store';
import { sendChatMessage, type ChatResponse, type AgentInfo } from '~/lib/modules/nexus/client';

const TEXTAREA_MIN_HEIGHT = 76;

interface BaseChatProps {
  textareaRef?: React.RefObject<HTMLTextAreaElement> | undefined;
  messageRef?: RefCallback<HTMLDivElement> | undefined;
  scrollRef?: RefCallback<HTMLDivElement> | undefined;
  showChat?: boolean;
  chatStarted?: boolean;
  isStreaming?: boolean;
  onStreamingChange?: (streaming: boolean) => void;
  messages?: Message[];
  description?: string;
  enhancingPrompt?: boolean;
  promptEnhanced?: boolean;
  input?: string;
  model?: string;
  setModel?: (model: string) => void;
  provider?: ProviderInfo;
  setProvider?: (provider: ProviderInfo) => void;
  providerList?: ProviderInfo[];
  handleStop?: () => void;
  sendMessage?: (event: React.UIEvent, messageInput?: string) => void;
  handleInputChange?: (event: React.ChangeEvent<HTMLTextAreaElement>) => void;
  enhancePrompt?: () => void;
  importChat?: (description: string, messages: Message[]) => Promise<void>;
  exportChat?: () => void;
  uploadedFiles?: File[];
  setUploadedFiles?: (files: File[]) => void;
  imageDataList?: string[];
  setImageDataList?: (dataList: string[]) => void;
  actionAlert?: ActionAlert;
  clearAlert?: () => void;
  supabaseAlert?: SupabaseAlert;
  clearSupabaseAlert?: () => void;
  deployAlert?: DeployAlert;
  clearDeployAlert?: () => void;
  llmErrorAlert?: LlmErrorAlertType;
  clearLlmErrorAlert?: () => void;
  data?: JSONValue[] | undefined;
  chatMode?: 'discuss' | 'build';
  setChatMode?: (mode: 'discuss' | 'build') => void;
  append?: (message: Message) => void;
  setMessages?: (messages: Message[] | ((messages: Message[]) => Message[])) => void;
  stop?: () => void;
  setNexusLastTarget?: (target: string | null) => void;
  addBmadMessages?: (messages: Message[]) => void;
  updateBmadMessage?: (messageId: string, content: string) => void;
  designScheme?: DesignScheme;
  setDesignScheme?: (scheme: DesignScheme) => void;
  selectedElement?: ElementInfo | null;
  setSelectedElement?: (element: ElementInfo | null) => void;
  addToolResult?: ({ toolCallId, result }: { toolCallId: string; result: any }) => void;
}

export const BaseChat = React.forwardRef<HTMLDivElement, BaseChatProps>(
  (
    {
      textareaRef,
      showChat = true,
      chatStarted = false,
      isStreaming = false,
      onStreamingChange,
      model,
      setModel,
      provider,
      setProvider,
      providerList,
      input = '',
      enhancingPrompt,
      handleInputChange,

      // promptEnhanced,
      enhancePrompt,
      sendMessage,
      handleStop,
      importChat,
      exportChat,
      uploadedFiles = [],
      setUploadedFiles,
      imageDataList = [],
      setImageDataList,
      messages = [],
      actionAlert,
      clearAlert,
      deployAlert,
      clearDeployAlert,
      supabaseAlert,
      clearSupabaseAlert,
      llmErrorAlert,
      clearLlmErrorAlert,
      data,
      chatMode,
      setChatMode,
      append,
      setMessages,
      stop,
      setNexusLastTarget,
      addBmadMessages,
      updateBmadMessage,
      designScheme,
      setDesignScheme,
      selectedElement,
      setSelectedElement,
      addToolResult = () => {
        throw new Error('addToolResult not implemented');
      },
    },
    ref,
  ) => {
    // Determine if chat is active (either chatStarted OR has messages)
    const isChatActive = chatStarted || (messages?.length ?? 0) > 0;
    const TEXTAREA_MAX_HEIGHT = isChatActive ? 400 : 200;
    const [apiKeys, setApiKeys] = useState<Record<string, string>>(getApiKeysFromCookies());
    const [modelList, setModelList] = useState<ModelInfo[]>([]);
    const [isModelSettingsCollapsed, setIsModelSettingsCollapsed] = useState(false);
    const [isListening, setIsListening] = useState(false);
    const [recognition, setRecognition] = useState<SpeechRecognition | null>(null);
    const [transcript, setTranscript] = useState('');
    const [isModelLoading, setIsModelLoading] = useState<string | undefined>('all');
    const [progressAnnotations, setProgressAnnotations] = useState<ProgressAnnotation[]>([]);
    const expoUrl = useStore(expoUrlAtom);
    const [qrModalOpen, setQrModalOpen] = useState(false);

    // Nexus orchestration state
    const isNexusEnabled = useStore(nexusModeEnabled);
    const nexusStatus = useStore(nexusConnectionStatus);
    const isNexusProcessingRef = React.useRef(false);
    const [nexusSessionId, setNexusSessionId] = useState<string | null>(null);
    const [nexusPhase, setNexusPhase] = useState<string>('');
    const [nexusBoltPrompt, setNexusBoltPrompt] = useState<string | null>(null);
    const [nexusActiveAgent, setNexusActiveAgent] = useState<AgentInfo | null>(null);

    useEffect(() => {
      if (expoUrl) {
        setQrModalOpen(true);
      }
    }, [expoUrl]);

    // Auto-collapse model settings when chat becomes active
    useEffect(() => {
      if (isChatActive && !isModelSettingsCollapsed) {
        console.log('[BaseChat] Auto-collapsing model settings - chat is active');
        setIsModelSettingsCollapsed(true);
      }
    }, [isChatActive, isModelSettingsCollapsed]);

    useEffect(() => {
      if (data) {
        const progressList = data.filter(
          (x) => typeof x === 'object' && (x as any).type === 'progress',
        ) as ProgressAnnotation[];
        setProgressAnnotations(progressList);
      }
    }, [data]);
    useEffect(() => {
      console.log(transcript);
    }, [transcript]);

    useEffect(() => {
      onStreamingChange?.(isStreaming);
    }, [isStreaming, onStreamingChange]);

    useEffect(() => {
      if (typeof window !== 'undefined' && ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onresult = (event) => {
          const transcript = Array.from(event.results)
            .map((result) => result[0])
            .map((result) => result.transcript)
            .join('');

          setTranscript(transcript);

          if (handleInputChange) {
            const syntheticEvent = {
              target: { value: transcript },
            } as React.ChangeEvent<HTMLTextAreaElement>;
            handleInputChange(syntheticEvent);
          }
        };

        recognition.onerror = (event) => {
          console.error('Speech recognition error:', event.error);
          setIsListening(false);
        };

        setRecognition(recognition);
      }
    }, []);

    useEffect(() => {
      if (typeof window !== 'undefined') {
        let parsedApiKeys: Record<string, string> | undefined = {};

        try {
          parsedApiKeys = getApiKeysFromCookies();
          setApiKeys(parsedApiKeys);
        } catch (error) {
          console.error('Error loading API keys from cookies:', error);
          Cookies.remove('apiKeys');
        }

        setIsModelLoading('all');
        fetch('/api/models')
          .then((response) => response.json())
          .then((data) => {
            const typedData = data as { modelList: ModelInfo[] };
            setModelList(typedData.modelList);
          })
          .catch((error) => {
            console.error('Error fetching model list:', error);
          })
          .finally(() => {
            setIsModelLoading(undefined);
          });
      }
    }, [providerList, provider]);

    const onApiKeysChange = async (providerName: string, apiKey: string) => {
      const newApiKeys = { ...apiKeys, [providerName]: apiKey };
      setApiKeys(newApiKeys);
      Cookies.set('apiKeys', JSON.stringify(newApiKeys));

      setIsModelLoading(providerName);

      let providerModels: ModelInfo[] = [];

      try {
        const response = await fetch(`/api/models/${encodeURIComponent(providerName)}`);
        const data = await response.json();
        providerModels = (data as { modelList: ModelInfo[] }).modelList;
      } catch (error) {
        console.error('Error loading dynamic models for:', providerName, error);
      }

      // Only update models for the specific provider
      setModelList((prevModels) => {
        const otherModels = prevModels.filter((model) => model.provider !== providerName);
        return [...otherModels, ...providerModels];
      });
      setIsModelLoading(undefined);
    };

    const startListening = () => {
      if (recognition) {
        recognition.start();
        setIsListening(true);
      }
    };

    const stopListening = () => {
      if (recognition) {
        recognition.stop();
        setIsListening(false);
      }
    };

    const handleSendMessage = async (event: React.UIEvent, messageInput?: string) => {
      // Store text before any modification
      const text = (messageInput || input || '').trim();

      // === VÉRIF 1: Log état Nexus au moment de l'envoi ===
      console.log('[handleSendMessage] START', {
        text: text?.substring(0, 50),
        isNexusEnabled,
        nexusStatus,
        nexusCheck: isNexusEnabled && nexusStatus === 'connected',
        isProcessing: isNexusProcessingRef.current,
        addBmadMessages: !!addBmadMessages,
        updateBmadMessage: !!updateBmadMessage,
      });

      // ALERT visible pour debug
      if (isNexusEnabled) {
        console.warn('[NEXUS DEBUG] Nexus IS ENABLED, status:', nexusStatus);
      } else {
        console.warn('[NEXUS DEBUG] Nexus is DISABLED');
      }

      // Guard: if no text, do nothing
      if (!text) {
        console.log('[handleSendMessage] No text, returning');
        return;
      }

      // Guard: if already processing, don't clear input, just return
      if (isNexusProcessingRef.current) {
        console.log('[handleSendMessage] BLOCKED - already processing');
        return;
      }

      // If Nexus is enabled and connected, use GUIDED CONVERSATION with AGENTS
      if (isNexusEnabled && nexusStatus === 'connected') {
        console.log('[Nexus] ✅ GUIDED CONVERSATION MODE - Multi-Agent');
        isNexusProcessingRef.current = true;

        // Stop any ongoing LLM requests
        stop?.();

        // Create user message immediately
        const userMessageId = crypto.randomUUID();
        const agentMessageId = `nexus-${crypto.randomUUID()}`;

        // Add user message to chat
        if (addBmadMessages) {
          const userMessage: Message = {
            id: userMessageId,
            role: 'user',
            content: text,
          };
          // Show thinking placeholder with current agent or orchestrator
          const thinkingAgent = nexusActiveAgent || { avatar: '🧭', name: 'Nexus' };
          const processingMessage: Message = {
            id: agentMessageId,
            role: 'assistant',
            content: `${thinkingAgent.avatar} _${thinkingAgent.name} réfléchit..._`,
          };
          addBmadMessages([userMessage, processingMessage]);
        }

        // Clear input immediately
        if (handleInputChange) {
          handleInputChange({ target: { value: '' } } as React.ChangeEvent<HTMLTextAreaElement>);
        }

        try {
          console.log('[Nexus] >>> Calling sendChatMessage...');

          // Send to multi-agent chat endpoint
          const response: ChatResponse = await sendChatMessage(
            text,
            nexusSessionId || undefined,
            'anonymous'
          );

          console.log('[Nexus] <<< Chat response:', response);

          // Store session ID and update active agent
          setNexusSessionId(response.session_id);
          setNexusPhase(response.phase);
          setNexusActiveAgent(response.agent);

          // If phase is "generation", we have the bolt_prompt
          if (response.phase === 'generation' && response.bolt_prompt) {
            setNexusBoltPrompt(response.bolt_prompt);
          }

          // Update the placeholder with agent's response
          if (updateBmadMessage) {
            const agent = response.agent;

            // Format: Avatar Name (Title) - Message
            let formattedMessage = `${agent.avatar} **${agent.name}** _${agent.title}_\n\n${response.message}`;

            // Add options if any
            if (response.options && response.options.length > 0) {
              formattedMessage += `\n\n---\n**Options:**\n`;
              response.options.forEach((opt, i) => {
                formattedMessage += `• ${opt}\n`;
              });
            }

            // If can advance to next phase
            if (response.can_advance) {
              formattedMessage += `\n\n---\n_✅ Tu peux taper **"continuer"** pour passer à l'étape suivante, ou pose d'autres questions._`;
            }

            // If we have a bolt_prompt ready
            if (response.bolt_prompt) {
              formattedMessage += `\n\n---\n🚀 **Prompt Bolt prêt!** Tape **"GO"** pour générer ton application.`;
            }

            updateBmadMessage(agentMessageId, formattedMessage);
          }

          // If user says GO and we have a bolt_prompt, send to LLM
          const goKeywords = ['go', 'génère', 'genere', 'lance', 'crée', 'cree', 'start'];
          const userWantsToGenerate = goKeywords.some(kw => text.toLowerCase().includes(kw));

          if (response.bolt_prompt && userWantsToGenerate) {
            console.log('[Nexus] 🚀 User confirmed - sending to Bolt LLM');
            setNexusLastTarget?.('bolt');

            // Add a system message indicating generation start
            if (addBmadMessages) {
              const genMessage: Message = {
                id: `gen-${crypto.randomUUID()}`,
                role: 'assistant',
                content: '🚀 **Génération en cours...** Bolt va maintenant créer ton application!',
              };
              addBmadMessages([genMessage]);
            }

            // Add the bolt prompt as a new message and send to LLM
            if (sendMessage) {
              sendMessage(event, response.bolt_prompt);
            }

            // Reset conversation for next project
            setNexusSessionId(null);
            setNexusPhase('');
            setNexusBoltPrompt(null);
            setNexusActiveAgent(null);
          }

          console.log('[Nexus] ✅ Chat handled');
          return; // EXIT - conversation handled

        } catch (error) {
          console.error('[Nexus] ❌ Chat error:', error);

          // Update the existing message with error
          const errorContent = `❌ **Erreur Agent**\n\n${error instanceof Error ? error.message : String(error)}\n\n_Vérifie que le meta-orchestrator est lancé._`;
          if (updateBmadMessage) {
            updateBmadMessage(agentMessageId, errorContent);
          }

          return; // EXIT on error
        } finally {
          // ALWAYS reset the processing flag
          isNexusProcessingRef.current = false;
          console.log('[Nexus] Processing flag reset');
        }
      }

      // Nexus disabled - direct LLM flow
      console.log('[Nexus DEBUG] Nexus disabled - direct LLM flow');
      if (sendMessage) {
        sendMessage(event, messageInput);
      }

      // Cleanup
      setSelectedElement?.(null);
      if (recognition) {
        recognition.abort();
        setTranscript('');
        setIsListening(false);
        if (handleInputChange) {
          const syntheticEvent = {
            target: { value: '' },
          } as React.ChangeEvent<HTMLTextAreaElement>;
          handleInputChange(syntheticEvent);
        }
      }
    };

    const handleFileUpload = () => {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';

      input.onchange = async (e) => {
        const file = (e.target as HTMLInputElement).files?.[0];

        if (file) {
          const reader = new FileReader();

          reader.onload = (e) => {
            const base64Image = e.target?.result as string;
            setUploadedFiles?.([...uploadedFiles, file]);
            setImageDataList?.([...imageDataList, base64Image]);
          };
          reader.readAsDataURL(file);
        }
      };

      input.click();
    };

    const handlePaste = async (e: React.ClipboardEvent) => {
      const items = e.clipboardData?.items;

      if (!items) {
        return;
      }

      for (const item of items) {
        if (item.type.startsWith('image/')) {
          e.preventDefault();

          const file = item.getAsFile();

          if (file) {
            const reader = new FileReader();

            reader.onload = (e) => {
              const base64Image = e.target?.result as string;
              setUploadedFiles?.([...uploadedFiles, file]);
              setImageDataList?.([...imageDataList, base64Image]);
            };
            reader.readAsDataURL(file);
          }

          break;
        }
      }
    };

    // Debug: Log state to trace intro visibility
    console.log('[BaseChat] Rendering - chatStarted:', chatStarted, 'messages.length:', messages.length, 'isChatActive:', isChatActive);

    const baseChat = (
      <div
        ref={ref}
        className={classNames(styles.BaseChat, 'relative flex h-full w-full overflow-hidden')}
        data-chat-visible={showChat}
      >
        <ClientOnly>{() => <Menu />}</ClientOnly>
        <div className="flex flex-col lg:flex-row overflow-y-auto w-full h-full">
          <div className={classNames(styles.Chat, 'flex flex-col flex-grow lg:min-w-[var(--chat-min-width)] h-full')}>
            {!isChatActive && (
              <div id="intro" className="mt-[16vh] max-w-2xl mx-auto text-center px-4 lg:px-0">
                <h1 className="text-3xl lg:text-6xl font-bold text-bolt-elements-textPrimary mb-4 animate-fade-in">
                  Where ideas begin
                </h1>
                <p className="text-md lg:text-xl mb-8 text-bolt-elements-textSecondary animate-fade-in animation-delay-200">
                  Bring ideas to life in seconds or get help on existing projects.
                </p>
              </div>
            )}
            <StickToBottom
              className={classNames('pt-6 px-2 sm:px-6 relative', {
                'h-full flex flex-col modern-scrollbar': isChatActive,
              })}
              resize="smooth"
              initial="smooth"
            >
              <StickToBottom.Content className="flex flex-col gap-4 relative ">
                <ClientOnly>
                  {() => {
                    return isChatActive ? (
                      <Messages
                        className="flex flex-col w-full flex-1 max-w-chat pb-4 mx-auto z-1"
                        messages={messages}
                        isStreaming={isStreaming}
                        append={append}
                        chatMode={chatMode}
                        setChatMode={setChatMode}
                        provider={provider}
                        model={model}
                        addToolResult={addToolResult}
                      />
                    ) : null;
                  }}
                </ClientOnly>
                <ScrollToBottom />
              </StickToBottom.Content>
              <div
                className={classNames('my-auto flex flex-col gap-2 w-full max-w-chat mx-auto z-prompt mb-6', {
                  'sticky bottom-2': isChatActive,
                })}
              >
                <div className="flex flex-col gap-2">
                  {deployAlert && (
                    <DeployChatAlert
                      alert={deployAlert}
                      clearAlert={() => clearDeployAlert?.()}
                      postMessage={(message: string | undefined) => {
                        sendMessage?.({} as any, message);
                        clearSupabaseAlert?.();
                      }}
                    />
                  )}
                  {supabaseAlert && (
                    <SupabaseChatAlert
                      alert={supabaseAlert}
                      clearAlert={() => clearSupabaseAlert?.()}
                      postMessage={(message) => {
                        sendMessage?.({} as any, message);
                        clearSupabaseAlert?.();
                      }}
                    />
                  )}
                  {actionAlert && (
                    <ChatAlert
                      alert={actionAlert}
                      clearAlert={() => clearAlert?.()}
                      postMessage={(message) => {
                        sendMessage?.({} as any, message);
                        clearAlert?.();
                      }}
                    />
                  )}
                  {llmErrorAlert && <LlmErrorAlert alert={llmErrorAlert} clearAlert={() => clearLlmErrorAlert?.()} />}
                </div>
                {progressAnnotations && <ProgressCompilation data={progressAnnotations} />}
                <ChatBox
                  isModelSettingsCollapsed={isModelSettingsCollapsed}
                  setIsModelSettingsCollapsed={setIsModelSettingsCollapsed}
                  provider={provider}
                  setProvider={setProvider}
                  providerList={providerList || (PROVIDER_LIST as ProviderInfo[])}
                  model={model}
                  setModel={setModel}
                  modelList={modelList}
                  apiKeys={apiKeys}
                  isModelLoading={isModelLoading}
                  onApiKeysChange={onApiKeysChange}
                  uploadedFiles={uploadedFiles}
                  setUploadedFiles={setUploadedFiles}
                  imageDataList={imageDataList}
                  setImageDataList={setImageDataList}
                  textareaRef={textareaRef}
                  input={input}
                  handleInputChange={handleInputChange}
                  handlePaste={handlePaste}
                  TEXTAREA_MIN_HEIGHT={TEXTAREA_MIN_HEIGHT}
                  TEXTAREA_MAX_HEIGHT={TEXTAREA_MAX_HEIGHT}
                  isStreaming={isStreaming}
                  handleStop={handleStop}
                  handleSendMessage={handleSendMessage}
                  enhancingPrompt={enhancingPrompt}
                  enhancePrompt={enhancePrompt}
                  isListening={isListening}
                  startListening={startListening}
                  stopListening={stopListening}
                  chatStarted={chatStarted}
                  exportChat={exportChat}
                  qrModalOpen={qrModalOpen}
                  setQrModalOpen={setQrModalOpen}
                  handleFileUpload={handleFileUpload}
                  chatMode={chatMode}
                  setChatMode={setChatMode}
                  designScheme={designScheme}
                  setDesignScheme={setDesignScheme}
                  selectedElement={selectedElement}
                  setSelectedElement={setSelectedElement}
                  isNexusEnabled={isNexusEnabled}
                  nexusStatus={nexusStatus}
                />
              </div>
            </StickToBottom>
            <div className="flex flex-col justify-center">
              {!isChatActive && (
                <div className="flex justify-center gap-2">
                  {ImportButtons(importChat)}
                  <GitCloneButton importChat={importChat} />
                </div>
              )}
              <div className="flex flex-col gap-5">
                {!isChatActive &&
                  ExamplePrompts((event, messageInput) => {
                    if (isStreaming) {
                      handleStop?.();
                      return;
                    }

                    handleSendMessage?.(event, messageInput);
                  })}
                {!isChatActive && <StarterTemplates />}
              </div>
            </div>
          </div>
          <ClientOnly>
            {() => (
              <Workbench chatStarted={chatStarted} isStreaming={isStreaming} setSelectedElement={setSelectedElement} />
            )}
          </ClientOnly>
        </div>
      </div>
    );

    return <Tooltip.Provider delayDuration={200}>{baseChat}</Tooltip.Provider>;
  },
);

function ScrollToBottom() {
  const { isAtBottom, scrollToBottom } = useStickToBottomContext();

  return (
    !isAtBottom && (
      <>
        <div className="sticky bottom-0 left-0 right-0 bg-gradient-to-t from-bolt-elements-background-depth-1 to-transparent h-20 z-10" />
        <button
          className="sticky z-50 bottom-0 left-0 right-0 text-4xl rounded-lg px-1.5 py-0.5 flex items-center justify-center mx-auto gap-2 bg-bolt-elements-background-depth-2 border border-bolt-elements-borderColor text-bolt-elements-textPrimary text-sm"
          onClick={() => scrollToBottom()}
        >
          Go to last message
          <span className="i-ph:arrow-down animate-bounce" />
        </button>
      </>
    )
  );
}
