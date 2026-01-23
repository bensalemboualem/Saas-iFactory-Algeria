'use client';

import Link from 'next/link';
import { Building, ArrowLeft, Sparkles, Star, ShieldCheck, Receipt, Briefcase, Zap, CreditCard, Phone, Rocket, Calculator, Users, Scale, Package, GraduationCap, Home } from 'lucide-react';
import { ToolCard, CategoryHeader } from '@/components/tools/ToolCard';
import { adminDzTools, getCriticalTools } from '@/lib/tools-data';

export default function AdminDzToolsPage() {
  // Stats
  const criticalTools = getCriticalTools(adminDzTools);
  const highPriorityTools = adminDzTools.filter(t => t.priority === 'high');
  const mediumPriorityTools = adminDzTools.filter(t => t.priority === 'medium');

  // Grouper par subcategory
  const securiteSociale = adminDzTools.filter(t => t.subcategory === 'securite-sociale');
  const fiscalite = adminDzTools.filter(t => t.subcategory === 'fiscalite');
  const entreprise = adminDzTools.filter(t => t.subcategory === 'entreprise');
  const servicesPublics = adminDzTools.filter(t => t.subcategory === 'services-publics');
  const emploi = adminDzTools.filter(t => t.subcategory === 'emploi');
  const documentsIdentite = adminDzTools.filter(t => t.subcategory === 'documents-identite');
  const telecom = adminDzTools.filter(t => t.subcategory === 'telecom');
  // Nouvelles sous-catégories Batch 2
  const juridique = adminDzTools.filter(t => t.subcategory === 'juridique');
  const douanes = adminDzTools.filter(t => t.subcategory === 'douanes');
  const education = adminDzTools.filter(t => t.subcategory === 'education');
  const logement = adminDzTools.filter(t => t.subcategory === 'logement');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/tools" className="text-gray-400 hover:text-gray-600">
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <Link href="/" className="flex items-center gap-2">
              <span className="text-2xl font-bold text-green-600">IAFactory</span>
              <span className="text-sm bg-green-100 text-green-800 px-2 py-0.5 rounded">Algeria</span>
            </Link>
          </div>
          <div className="flex items-center gap-4">
            <div className="bg-gray-100 px-3 py-1.5 rounded-lg text-sm">
              <span className="text-gray-500">Crédits:</span>
              <span className="font-semibold text-gray-900 ml-1">847</span>
            </div>
          </div>
        </nav>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Category Header */}
        <CategoryHeader
          icon={Building}
          title="Administration Algérie"
          description={`${adminDzTools.length} assistants IA pour simplifier vos démarches administratives algériennes`}
          toolCount={adminDzTools.length}
          criticalCount={criticalTools.length}
          isExclusive={true}
        />

        {/* Stats Banner */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-emerald-600">{adminDzTools.length}</div>
            <div className="text-sm text-gray-500">Outils total</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-red-600">{criticalTools.length}</div>
            <div className="text-sm text-gray-500">Critiques</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-orange-600">{highPriorityTools.length}</div>
            <div className="text-sm text-gray-500">Haute priorité</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-yellow-600">{mediumPriorityTools.length}</div>
            <div className="text-sm text-gray-500">Moyenne priorité</div>
          </div>
          <div className="bg-white rounded-xl p-4 border border-gray-200 text-center">
            <div className="text-3xl font-bold text-green-600">100%</div>
            <div className="text-sm text-gray-500">Exclusifs DZ</div>
          </div>
        </div>

        {/* Banner Exclusif */}
        <div className="bg-gradient-to-r from-green-600 to-emerald-600 rounded-xl p-6 mb-10 text-white">
          <div className="flex items-center gap-4">
            <span className="text-5xl">🇩🇿</span>
            <div>
              <h3 className="font-bold text-xl">Outils EXCLUSIFS Algérie - Notre USP #1</h3>
              <p className="opacity-90 mt-1">
                Ces assistants n'existent NULLE PART ailleurs. GravityWrite, Jasper, Copy.ai = ZÉRO outil pour l'Algérie.
                Simplifiez vos démarches CNAS, CASNOS, impôts, registre du commerce, Sonelgaz et plus !
              </p>
            </div>
          </div>
        </div>

        {/* Outils Critiques */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-red-500" />
            <h2 className="text-xl font-semibold">Outils Critiques</h2>
            <span className="bg-red-100 text-red-700 px-2 py-0.5 rounded-full text-xs font-medium">
              Essentiels
            </span>
          </div>
          <p className="text-gray-600 mb-4">Les assistants les plus utilisés pour les démarches algériennes</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
            {criticalTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/admin-dz" />
            ))}
          </div>
        </section>

        {/* Section Sécurité Sociale */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <ShieldCheck className="w-5 h-5 text-blue-600" />
            <h2 className="text-xl font-semibold">Sécurité Sociale & Retraite</h2>
            <span className="text-sm font-normal text-gray-500">
              ({securiteSociale.length} assistants)
            </span>
          </div>
          <p className="text-gray-600 mb-4">CNAS, CASNOS, CNR, allocations familiales et couverture maladie</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {securiteSociale.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/admin-dz" />
            ))}
          </div>
        </section>

        {/* Section Fiscalité */}
        {fiscalite.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Receipt className="w-5 h-5 text-purple-600" />
              <h2 className="text-xl font-semibold">Fiscalité</h2>
              <span className="text-sm font-normal text-gray-500">
                ({fiscalite.length} assistants)
              </span>
            </div>
            <p className="text-gray-600 mb-4">IRG, IBS, TVA, TAP, déclarations G50 et optimisation fiscale</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {fiscalite.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/admin-dz" />
              ))}
            </div>
          </section>
        )}

        {/* Section Création d'Entreprise */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <Rocket className="w-5 h-5 text-orange-600" />
            <h2 className="text-xl font-semibold">Création d'Entreprise</h2>
            <span className="text-sm font-normal text-gray-500">
              ({entreprise.length} assistants)
            </span>
          </div>
          <p className="text-gray-600 mb-4">CNRC, ANSEJ, CNAC, ANGEM, douanes et financement de projets</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {entreprise.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/admin-dz" />
            ))}
          </div>
        </section>

        {/* Section Services Publics */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <Zap className="w-5 h-5 text-yellow-600" />
            <h2 className="text-xl font-semibold">Services Publics</h2>
            <span className="text-sm font-normal text-gray-500">
              ({servicesPublics.length} assistants)
            </span>
          </div>
          <p className="text-gray-600 mb-4">Sonelgaz, SEAAL, Algérie Télécom, banques et logement</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {servicesPublics.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/admin-dz" />
            ))}
          </div>
        </section>

        {/* Section Emploi */}
        {emploi.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Briefcase className="w-5 h-5 text-teal-600" />
              <h2 className="text-xl font-semibold">Emploi</h2>
              <span className="text-sm font-normal text-gray-500">
                ({emploi.length} assistants)
              </span>
            </div>
            <p className="text-gray-600 mb-4">ANEM, DAIP, formations et recherche d'emploi</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {emploi.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/admin-dz" />
              ))}
            </div>
          </section>
        )}

        {/* Section Documents d'Identité */}
        <section className="mb-10">
          <div className="flex items-center gap-2 mb-4">
            <CreditCard className="w-5 h-5 text-indigo-600" />
            <h2 className="text-xl font-semibold">Documents d'Identité</h2>
            <span className="text-sm font-normal text-gray-500">
              ({documentsIdentite.length} assistants)
            </span>
          </div>
          <p className="text-gray-600 mb-4">Passeport, CNI, permis de conduire, carte grise, état civil</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {documentsIdentite.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/admin-dz" />
            ))}
          </div>
        </section>

        {/* Section Télécom */}
        {telecom.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Phone className="w-5 h-5 text-pink-600" />
              <h2 className="text-xl font-semibold">Télécommunications</h2>
              <span className="text-sm font-normal text-gray-500">
                ({telecom.length} assistants)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Mobilis, Djezzy, Ooredoo - forfaits et services</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {telecom.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/admin-dz" />
              ))}
            </div>
          </section>
        )}

        {/* Section Juridique - NOUVEAU */}
        {juridique.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Scale className="w-5 h-5 text-amber-600" />
              <h2 className="text-xl font-semibold">Juridique & Contrats</h2>
              <span className="text-sm font-normal text-gray-500">
                ({juridique.length} assistants)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Conseils juridiques, contrats de location, statuts d'entreprise</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {juridique.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/admin-dz" />
              ))}
            </div>
          </section>
        )}

        {/* Section Douanes - NOUVEAU */}
        {douanes.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Package className="w-5 h-5 text-cyan-600" />
              <h2 className="text-xl font-semibold">Douanes & Import/Export</h2>
              <span className="text-sm font-normal text-gray-500">
                ({douanes.length} assistants)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Calcul droits de douane, dédouanement, import/export</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {douanes.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/admin-dz" />
              ))}
            </div>
          </section>
        )}

        {/* Section Education - NOUVEAU */}
        {education.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <GraduationCap className="w-5 h-5 text-violet-600" />
              <h2 className="text-xl font-semibold">Scolarité & Education</h2>
              <span className="text-sm font-normal text-gray-500">
                ({education.length} assistants)
              </span>
            </div>
            <p className="text-gray-600 mb-4">Inscriptions scolaires, bourses, certificats, orientation</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {education.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/admin-dz" />
              ))}
            </div>
          </section>
        )}

        {/* Section Logement - NOUVEAU */}
        {logement.length > 0 && (
          <section className="mb-10">
            <div className="flex items-center gap-2 mb-4">
              <Home className="w-5 h-5 text-rose-600" />
              <h2 className="text-xl font-semibold">Logement</h2>
              <span className="text-sm font-normal text-gray-500">
                ({logement.length} assistants)
              </span>
            </div>
            <p className="text-gray-600 mb-4">AADL, LPP, logement social, aides CNL</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {logement.map(tool => (
                <ToolCard key={tool.id} tool={tool} basePath="/tools/admin-dz" />
              ))}
            </div>
          </section>
        )}

        {/* Workflow Suggéré */}
        <section className="mb-10 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-green-600" />
            Parcours Création d'Entreprise
          </h3>
          <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">1. CNRC (Registre commerce)</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">2. Impôts (NIF)</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">3. CASNOS/CNAS</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">4. Banque (Compte pro)</span>
            <span className="text-gray-400">→</span>
            <span className="bg-white px-3 py-1.5 rounded-lg border shadow-sm">5. ANSEJ/CNAC (Si financement)</span>
          </div>
          <p className="text-gray-600 text-sm mt-4">
            Suivez ce parcours pour créer votre entreprise en Algérie de A à Z.
          </p>
        </section>

        {/* Tips Section */}
        <section className="mb-10 bg-gradient-to-r from-emerald-50 to-teal-50 rounded-xl p-6 border border-emerald-200">
          <h3 className="font-semibold text-emerald-900 mb-3">Conseils pour vos démarches administratives</h3>
          <ul className="text-sm text-emerald-800 space-y-2">
            <li>• Préparez TOUJOURS une copie de votre CNI et un justificatif de domicile récent</li>
            <li>• Les extraits de naissance (S12) sont valables 3 mois - anticipez !</li>
            <li>• Utilisez les services en ligne quand disponibles : cnas.dz, cnrc.dz, mf.gov.dz</li>
            <li>• Conservez TOUS vos récépissés et numéros de dossier</li>
            <li>• Les horaires des administrations : Dimanche-Jeudi, 8h-16h (souvent fermé le vendredi)</li>
          </ul>
        </section>

        {/* Tous les outils */}
        <section className="mt-12 pt-8 border-t border-gray-200">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Star className="w-5 h-5 text-yellow-500" />
            Tous les assistants Admin DZ ({adminDzTools.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {adminDzTools.map(tool => (
              <ToolCard key={tool.id} tool={tool} basePath="/tools/admin-dz" />
            ))}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 px-4 mt-12">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-gray-400">
            © 2026 IAFactory Algeria • Conçu en Algérie 🇩🇿
          </p>
        </div>
      </footer>
    </div>
  );
}
