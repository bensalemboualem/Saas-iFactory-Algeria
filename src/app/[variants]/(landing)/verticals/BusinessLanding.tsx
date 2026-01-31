'use client';

import { Button, Icon } from '@lobehub/ui';
import { Collapse, CollapseProps } from 'antd';
import { createStyles } from 'antd-style';
import {
  BarChart3,
  Briefcase,
  Check,
  ChevronRight,
  CreditCard,
  FileSpreadsheet,
  Globe,
  Layers,
  Lock,
  Mail,
  PenTool,
  Server,
  Sparkles,
  Users,
} from 'lucide-react';
import { memo } from 'react';
import { Center, Flexbox } from 'react-layout-kit';
import { useNavigate } from 'react-router-dom';

const useStyles = createStyles(({ css, token, responsive }) => ({
  container: css`
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
    ${responsive.mobile} {
      padding: 0 16px;
    }
  `,
  ctaFinal: css`
    padding: 60px 40px;
    text-align: center;
    background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
    border-radius: ${token.borderRadiusLG}px;
    ${responsive.mobile} {
      padding: 40px 20px;
    }
  `,
  ctaFinalSubtitle: css`
    max-width: 500px;
    margin: 0 auto 32px;
    font-size: 18px;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.9);
    ${responsive.mobile} {
      font-size: 16px;
    }
  `,
  ctaFinalTitle: css`
    margin: 0 0 16px;
    font-size: 32px;
    font-weight: 700;
    color: #fff;
    ${responsive.mobile} {
      font-size: 24px;
    }
  `,
  diffBlock: css`
    flex: 1;
    min-width: 280px;
    padding: 32px;
    text-align: center;
    background: ${token.colorBgContainer};
    border: 1px solid ${token.colorBorderSecondary};
    border-radius: ${token.borderRadiusLG}px;
  `,
  diffDescription: css`
    margin: 0;
    font-size: 14px;
    line-height: 1.6;
    color: ${token.colorTextSecondary};
  `,
  diffIcon: css`
    display: flex;
    align-items: center;
    justify-content: center;
    width: 64px;
    height: 64px;
    margin: 0 auto 16px;
    background: linear-gradient(135deg, #7c3aed20 0%, #a855f720 100%);
    border-radius: 50%;
    color: #7c3aed;
  `,
  diffTitle: css`
    margin: 0 0 12px;
    font-size: 20px;
    font-weight: 600;
    color: ${token.colorText};
  `,
  faqPanel: css`
    .ant-collapse-header {
      font-size: 16px;
      font-weight: 500;
    }
    .ant-collapse-content-box {
      font-size: 14px;
      line-height: 1.6;
      color: ${token.colorTextSecondary};
    }
  `,
  hero: css`
    padding: 80px 0 60px;
    text-align: center;
    background: linear-gradient(180deg, #7c3aed08 0%, transparent 100%);
    ${responsive.mobile} {
      padding: 48px 0 40px;
    }
  `,
  heroButtons: css`
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    justify-content: center;
    ${responsive.mobile} {
      flex-direction: column;
      align-items: center;
    }
  `,
  heroSubtitle: css`
    max-width: 700px;
    margin: 0 auto 40px;
    font-size: 18px;
    line-height: 1.6;
    color: ${token.colorTextSecondary};
    ${responsive.mobile} {
      margin-bottom: 32px;
      font-size: 16px;
    }
  `,
  heroTitle: css`
    margin: 0 0 24px;
    font-size: 48px;
    font-weight: 800;
    line-height: 1.2;
    color: #7c3aed;
    ${responsive.mobile} {
      font-size: 28px;
    }
  `,
  page: css`
    overflow-x: hidden;
    overflow-y: auto;
    width: 100%;
    min-height: 100vh;
    background: ${token.colorBgLayout};
  `,
  proofBar: css`
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    justify-content: center;
    padding: 24px;
    background: ${token.colorBgContainer};
    border: 1px solid ${token.colorBorderSecondary};
    border-radius: ${token.borderRadiusLG}px;
    ${responsive.mobile} {
      gap: 16px;
      padding: 16px;
    }
  `,
  proofItem: css`
    display: flex;
    gap: 8px;
    align-items: center;
    font-size: 14px;
    font-weight: 500;
    color: ${token.colorText};
  `,
  section: css`
    padding: 60px 0;
    ${responsive.mobile} {
      padding: 40px 0;
    }
  `,
  sectionTitle: css`
    margin: 0 0 40px;
    font-size: 32px;
    font-weight: 700;
    color: ${token.colorText};
    text-align: center;
    ${responsive.mobile} {
      margin-bottom: 24px;
      font-size: 24px;
    }
  `,
  tag: css`
    display: inline-block;
    padding: 4px 12px;
    margin-bottom: 16px;
    font-size: 12px;
    font-weight: 600;
    color: #7c3aed;
    text-transform: uppercase;
    letter-spacing: 1px;
    background: #7c3aed15;
    border-radius: 20px;
  `,
  useCaseCard: css`
    cursor: pointer;
    flex: 1;
    min-width: 240px;
    padding: 24px;
    background: ${token.colorBgContainer};
    border: 1px solid ${token.colorBorderSecondary};
    border-radius: ${token.borderRadiusLG}px;
    transition: all 0.3s ease;
    &:hover {
      border-color: #7c3aed;
      box-shadow: 0 4px 16px #7c3aed15;
      transform: translateY(-2px);
    }
  `,
  useCaseDescription: css`
    margin: 0 0 16px;
    font-size: 14px;
    line-height: 1.5;
    color: ${token.colorTextSecondary};
  `,
  useCaseIcon: css`
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    margin-bottom: 16px;
    background: #7c3aed15;
    border-radius: ${token.borderRadius}px;
    color: #7c3aed;
  `,
  useCaseLink: css`
    display: flex;
    gap: 4px;
    align-items: center;
    font-size: 14px;
    font-weight: 500;
    color: #7c3aed;
  `,
  useCaseTitle: css`
    margin: 0 0 8px;
    font-size: 18px;
    font-weight: 600;
    color: ${token.colorText};
  `,
}));

const BusinessLanding = memo(() => {
  const { styles } = useStyles();
  const navigate = useNavigate();

  const handleNavigate = (path: string) => {
    navigate(path);
  };

  const faqItems: CollapseProps['items'] = [
    {
      children: (
        <p>
          Nous acceptons les paiements en DZD via carte bancaire, virement IBAN, et facture pour les
          entreprises. TVA algérienne incluse.
        </p>
      ),
      key: '1',
      label: 'Comment fonctionne la facturation ?',
    },
    {
      children: (
        <p>
          Oui, nous proposons des plans équipe avec gestion centralisée des utilisateurs, facturation
          unique et statistiques d'utilisation par collaborateur.
        </p>
      ),
      key: '2',
      label: 'Peut-on avoir plusieurs utilisateurs ?',
    },
    {
      children: (
        <p>
          Absolument. Le mode local avec Ollama permet de traiter les documents sensibles sans
          qu'ils quittent votre infrastructure. Idéal pour la confidentialité des affaires.
        </p>
      ),
      key: '3',
      label: 'Mes données commerciales sont-elles sécurisées ?',
    },
    {
      children: (
        <p>
          Oui, IAFactory s'intègre facilement avec vos outils existants via notre API. Compatible
          avec les principaux CRM, ERP et systèmes documentaires.
        </p>
      ),
      key: '4',
      label: "L'outil s'intègre-t-il à nos systèmes existants ?",
    },
    {
      children: (
        <p>
          Oui, vous pouvez créer des bases de connaissances avec vos procédures internes, catalogues
          produits et FAQ pour des réponses adaptées à votre entreprise.
        </p>
      ),
      key: '5',
      label: 'Peut-on personnaliser les réponses pour notre entreprise ?',
    },
  ];

  return (
    <div className={styles.page}>
      {/* HERO SECTION */}
      <section className={styles.hero}>
        <div className={styles.container}>
          <span className={styles.tag}>PME & Entreprises</span>
          <h1 className={styles.heroTitle}>L'IA qui automatise vos tâches administratives</h1>
          <p className={styles.heroSubtitle}>
            Emails, rapports, documents, analyse de données. Gagnez des heures chaque semaine en
            automatisant les tâches répétitives de votre PME.
          </p>
          <div className={styles.heroButtons}>
            <Button
              icon={<Icon icon={Briefcase} />}
              onClick={() => handleNavigate('/signup')}
              size="large"
              style={{ background: '#7c3aed', borderColor: '#7c3aed' }}
              type="primary"
            >
              Essayer gratuitement
            </Button>
            <Button onClick={() => handleNavigate('/profile/usage')} size="large">
              Tarifs entreprises
            </Button>
          </div>
        </div>
      </section>

      {/* PROOF BAR */}
      <section className={styles.container}>
        <div className={styles.proofBar}>
          <div className={styles.proofItem}>
            <Icon icon={CreditCard} />
            <span>Facturation DZD</span>
          </div>
          <div className={styles.proofItem}>
            <Icon icon={Users} />
            <span>Plans équipe</span>
          </div>
          <div className={styles.proofItem}>
            <Icon icon={Server} />
            <span>Hébergement Algérie</span>
          </div>
          <div className={styles.proofItem}>
            <Icon icon={Lock} />
            <span>Données confidentielles</span>
          </div>
        </div>
      </section>

      {/* USE CASES */}
      <section className={styles.section}>
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Automatisez votre quotidien</h2>
          <Flexbox gap={24} horizontal style={{ flexWrap: 'wrap' }}>
            <div className={styles.useCaseCard} onClick={() => handleNavigate('/chat')}>
              <div className={styles.useCaseIcon}>
                <Icon icon={Mail} size={24} />
              </div>
              <h3 className={styles.useCaseTitle}>Emails professionnels</h3>
              <p className={styles.useCaseDescription}>
                Rédigez des emails parfaits en quelques secondes, en français, arabe et darija.
              </p>
              <div className={styles.useCaseLink}>
                Commencer <Icon icon={ChevronRight} size={16} />
              </div>
            </div>
            <div className={styles.useCaseCard} onClick={() => handleNavigate('/chat')}>
              <div className={styles.useCaseIcon}>
                <Icon icon={FileSpreadsheet} size={24} />
              </div>
              <h3 className={styles.useCaseTitle}>Rapports & documents</h3>
              <p className={styles.useCaseDescription}>
                Générez rapports, procès-verbaux et documents administratifs automatiquement.
              </p>
              <div className={styles.useCaseLink}>
                Commencer <Icon icon={ChevronRight} size={16} />
              </div>
            </div>
            <div className={styles.useCaseCard} onClick={() => handleNavigate('/chat')}>
              <div className={styles.useCaseIcon}>
                <Icon icon={BarChart3} size={24} />
              </div>
              <h3 className={styles.useCaseTitle}>Analyse de données</h3>
              <p className={styles.useCaseDescription}>
                Analysez vos données, créez des synthèses et identifiez les tendances clés.
              </p>
              <div className={styles.useCaseLink}>
                Commencer <Icon icon={ChevronRight} size={16} />
              </div>
            </div>
            <div className={styles.useCaseCard} onClick={() => handleNavigate('/knowledge')}>
              <div className={styles.useCaseIcon}>
                <Icon icon={PenTool} size={24} />
              </div>
              <h3 className={styles.useCaseTitle}>Contenu marketing</h3>
              <p className={styles.useCaseDescription}>
                Créez du contenu pour vos réseaux sociaux, site web et communications clients.
              </p>
              <div className={styles.useCaseLink}>
                Commencer <Icon icon={ChevronRight} size={16} />
              </div>
            </div>
          </Flexbox>
        </div>
      </section>

      {/* FEATURES */}
      <section className={styles.section}>
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Conçu pour les PME algériennes</h2>
          <Flexbox gap={24} horizontal style={{ flexWrap: 'wrap' }}>
            <div className={styles.diffBlock}>
              <div className={styles.diffIcon}>
                <Icon icon={Globe} size={28} />
              </div>
              <h3 className={styles.diffTitle}>Multilingue professionnel</h3>
              <p className={styles.diffDescription}>
                Communiquez avec vos clients et partenaires en français, arabe et darija avec un ton
                professionnel adapté.
              </p>
            </div>
            <div className={styles.diffBlock}>
              <div className={styles.diffIcon}>
                <Icon icon={Layers} size={28} />
              </div>
              <h3 className={styles.diffTitle}>Base de connaissances</h3>
              <p className={styles.diffDescription}>
                Créez votre propre base documentaire pour des réponses adaptées à votre entreprise,
                vos produits et vos procédures.
              </p>
            </div>
            <div className={styles.diffBlock}>
              <div className={styles.diffIcon}>
                <Icon icon={Sparkles} size={28} />
              </div>
              <h3 className={styles.diffTitle}>Meilleurs modèles IA</h3>
              <p className={styles.diffDescription}>
                Accès à GPT-4, Claude, Gemini et autres. Choisissez le modèle optimal pour chaque
                tâche.
              </p>
            </div>
          </Flexbox>
        </div>
      </section>

      {/* FAQ */}
      <section className={styles.section}>
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Questions fréquentes</h2>
          <Collapse
            className={styles.faqPanel}
            expandIconPosition="end"
            items={faqItems}
            size="large"
          />
        </div>
      </section>

      {/* CTA FINAL */}
      <section className={styles.section}>
        <div className={styles.container}>
          <div className={styles.ctaFinal}>
            <h2 className={styles.ctaFinalTitle}>Boostez la productivité de votre équipe</h2>
            <p className={styles.ctaFinalSubtitle}>
              Rejoignez les PME algériennes qui gagnent du temps grâce à l'IA.
            </p>
            <Button
              icon={<Icon icon={Check} />}
              onClick={() => handleNavigate('/signup')}
              size="large"
              style={{
                background: '#fff',
                borderColor: '#fff',
                color: '#7c3aed',
              }}
            >
              Créer un compte gratuit
            </Button>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <Center padding={40}>
        <Flexbox align="center" gap={16}>
          <Flexbox gap={8} horizontal style={{ color: 'rgba(0,0,0,0.45)', fontSize: 14 }}>
            <Briefcase size={16} />
            <span>IAFactory Business - L'IA pour les PME algériennes</span>
          </Flexbox>
        </Flexbox>
      </Center>
    </div>
  );
});

BusinessLanding.displayName = 'BusinessLanding';

export default BusinessLanding;
