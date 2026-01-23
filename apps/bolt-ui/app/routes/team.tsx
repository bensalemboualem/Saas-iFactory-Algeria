import { json, type ActionFunctionArgs } from '@remix-run/cloudflare';
import { Form, useActionData, useNavigation } from '@remix-run/react';
import { Header } from '~/components/header/Header';

export const action = async ({ request }: ActionFunctionArgs) => {
    const formData = await request.formData();
    const email = formData.get('email');
    const role = formData.get('role');

    // TODO: Connect to Real Backend (Postgres/Supabase)
    // For now, simulate success
    return json({ success: true, email, role });
};

export default function TeamPage() {
    const actionData = useActionData<typeof action>();
    const navigation = useNavigation();
    const isSubmitting = navigation.state === 'submitting';

    return (
        <div className="flex flex-col h-full bg-bolt-elements-background-depth-1 text-bolt-elements-textPrimary">
            <Header />

            <main className="flex-1 overflow-y-auto p-4 md:p-8">
                <div className="max-w-4xl mx-auto">
                    <h1 className="text-3xl font-bold mb-6 flex items-center gap-3">
                        <div className="i-ph:users-three-duotone text-accent-500" />
                        Gestion d'Équipe (Nexus Squad)
                    </h1>

                    <div className="grid md:grid-cols-2 gap-8">
                        {/* Invite Form */}
                        <div className="bg-bolt-elements-background-depth-2 p-6 rounded-lg border border-bolt-elements-borderColor shadow-sm">
                            <h2 className="text-xl font-semibold mb-4">Inviter un Collaborateur</h2>

                            {actionData?.success ? (
                                <div className="p-4 bg-green-500/10 border border-green-500/20 text-green-500 rounded-md mb-4 flex items-center gap-2">
                                    <div className="i-ph:check-circle-fill" />
                                    Invitation envoyée à {actionData.email} !
                                    <a href="/team" className="ml-auto underline text-sm">Envoyer une autre</a>
                                </div>
                            ) : (
                                <Form method="post" className="flex flex-col gap-4">
                                    <div>
                                        <label className="block text-sm font-medium mb-1">Email Professionnel</label>
                                        <input
                                            type="email"
                                            name="email"
                                            required
                                            placeholder="collegue@iafactory.dz"
                                            className="w-full bg-bolt-elements-background-depth-1 border border-bolt-elements-borderColor rounded-md p-2 focus:border-accent-500 outline-none"
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-sm font-medium mb-1">Rôle</label>
                                        <select
                                            name="role"
                                            className="w-full bg-bolt-elements-background-depth-1 border border-bolt-elements-borderColor rounded-md p-2 focus:border-accent-500 outline-none"
                                        >
                                            <option value="viewer">Observateur</option>
                                            <option value="editor">Éditeur (Prompt & Code)</option>
                                            <option value="admin">Admin d'Équipe</option>
                                        </select>
                                    </div>

                                    <button
                                        type="submit"
                                        disabled={isSubmitting}
                                        className="mt-2 bg-accent-500 hover:bg-accent-600 text-white font-medium py-2 px-4 rounded-md flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
                                    >
                                        {isSubmitting ? (
                                            <div className="i-svg-spinners:90-ring-with-bg animate-spin" />
                                        ) : (
                                            <div className="i-ph:paper-plane-right-fill" />
                                        )}
                                        Envoyer l'Invitation
                                    </button>
                                </Form>
                            )}
                        </div>

                        {/* Team List (Mock) */}
                        <div className="bg-bolt-elements-background-depth-2 p-6 rounded-lg border border-bolt-elements-borderColor shadow-sm">
                            <h2 className="text-xl font-semibold mb-4">Membres Actifs</h2>
                            <div className="space-y-4">
                                {[
                                    { name: 'Toi (Admin)', email: 'admin@nexus.dz', role: 'Propriétaire', avatar: 'bg-purple-500' },
                                    { name: 'Karim Dev', email: 'karim@iafactory.dz', role: 'Éditeur', avatar: 'bg-blue-500' },
                                    { name: 'Sarah Design', email: 'sarah@iafactory.dz', role: 'Observateur', avatar: 'bg-pink-500' },
                                ].map((member, i) => (
                                    <div key={i} className="flex items-center gap-3 p-3 hover:bg-bolt-elements-background-depth-1 rounded-md transition-colors">
                                        <div className={`w-10 h-10 rounded-full ${member.avatar} flex items-center justify-center text-white font-bold`}>
                                            {member.name[0]}
                                        </div>
                                        <div>
                                            <div className="font-medium">{member.name}</div>
                                            <div className="text-xs text-bolt-elements-textTertiary">{member.role} • {member.email}</div>
                                        </div>
                                        <button className="ml-auto text-bolt-elements-textTertiary hover:text-red-500">
                                            <div className="i-ph:trash" />
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
