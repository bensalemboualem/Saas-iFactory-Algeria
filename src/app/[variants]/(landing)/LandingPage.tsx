'use client';

import { Button, Icon } from '@lobehub/ui';
import { Collapse, CollapseProps } from 'antd';
import { createStyles } from 'antd-style';
import {
  BookOpen,
  BriefcaseBusiness,
  Check,
  ChevronRight,
  CreditCard,
  FileText,
  Globe,
  Layers,
  Lock,
  Palette,
  Rocket,
  Server,
  Sparkles,
  Users,
  Zap,
} from 'lucide-react';
import { memo } from 'react';
import { Center, Flexbox } from 'react-layout-kit';
import { useNavigate } from 'react-router-dom';

const useStyles = createStyles(({ css, token, responsive }) => ({
  card: css`
    cursor: pointer;

    padding: 24px;

    background: ${token.colorBgContainer};
    border: 1px solid ${token.colorBorderSecondary};
    border-radius: ${token.borderRadiusLG}px;

    transition: all 0.3s ease;

    &:hover {
      border-color: ${token.colorPrimary};
      box-shadow: 0 4px 16px ${token.colorPrimaryBg};
      transform: translateY(-2px);
    }
  `,
  cardDescription: css`
    margin: 0;
    font-size: 14px;
    line-height: 1.5;
    color: ${token.colorTextSecondary};
  `,
  cardIcon: css`
    display: flex;
    align-items: center;
    justify-content: center;

    width: 48px;
    height: 48px;

    background: ${token.colorPrimaryBg};
    border-radius: ${token.borderRadius}px;
  `,
  cardTitle: css`
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: ${token.colorText};
  `,
  container: css`
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;

    ${responsive.mobile} {
      padding: 0 16px;
    }
  `,
  creditsBlock: css`
    padding: 40px;

    text-align: center;

    background: linear-gradient(135deg, ${token.colorPrimaryBg} 0%, ${token.colorBgContainer} 100%);
    border: 1px solid ${token.colorBorderSecondary};
    border-radius: ${token.borderRadiusLG}px;

    ${responsive.mobile} {
      padding: 24px;
    }
  `,
  creditsDescription: css`
    max-width: 600px;
    margin: 0 auto 24px;
    font-size: 16px;
    line-height: 1.6;
    color: ${token.colorTextSecondary};
  `,
  creditsTitle: css`
    margin: 0 0 16px;
    font-size: 28px;
    font-weight: 700;
    color: ${token.colorText};

    ${responsive.mobile} {
      font-size: 22px;
    }
  `,
  ctaFinal: css`
    padding: 60px 40px;

    text-align: center;

    background: linear-gradient(135deg, ${token.colorPrimary} 0%, ${token.colorPrimaryActive} 100%);
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

    background: ${token.colorPrimaryBg};
    border-radius: 50%;
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
    color: ${token.colorText};

    ${responsive.mobile} {
      font-size: 28px;
    }
  `,
  howCard: css`
    flex: 1;
    min-width: 200px;
    padding: 32px 24px;

    text-align: center;

    background: ${token.colorBgContainer};
    border: 1px solid ${token.colorBorderSecondary};
    border-radius: ${token.borderRadiusLG}px;
  `,
  howDescription: css`
    margin: 0;
    font-size: 14px;
    color: ${token.colorTextSecondary};
  `,
  howNumber: css`
    display: flex;
    align-items: center;
    justify-content: center;

    width: 40px;
    height: 40px;
    margin: 0 auto 16px;

    font-size: 18px;
    font-weight: 700;
    color: ${token.colorPrimary};

    background: ${token.colorPrimaryBg};
    border-radius: 50%;
  `,
  howTitle: css`
    margin: 0 0 8px;
    font-size: 18px;
    font-weight: 600;
    color: ${token.colorText};
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
      border-color: ${token.colorPrimary};
      box-shadow: 0 4px 16px ${token.colorPrimaryBg};
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

    background: ${token.colorPrimaryBg};
    border-radius: ${token.borderRadius}px;
  `,
  useCaseLink: css`
    display: flex;
    gap: 4px;
    align-items: center;

    font-size: 14px;
    font-weight: 500;
    color: ${token.colorPrimary};
  `,
  useCaseTitle: css`
    margin: 0 0 8px;
    font-size: 18px;
    font-weight: 600;
    color: ${token.colorText};
  `,
}));

const LandingPage = memo(() => {
  const { styles } = useStyles();
  const navigate = useNavigate();

  const handleNavigate = (path: string) => {
    navigate(path);
  };

  const faqItems: CollapseProps['items'] = [
    {
      children: (
        <p>
          Nous acceptons les paiements en dinars algériens (DZD) par carte bancaire, virement IBAN,
          ou facture pour les entreprises. TVA algérienne incluse.
        </p>
      ),
      key: '1',
      label: 'Comment je paye ?',
    },
    {
      children: (
        <p>
          Non, le service fonctionne avec un système de crédits. Vous achetez des crédits et les
          utilisez selon vos besoins. Chaque modèle IA consomme un nombre différent de crédits selon
          sa puissance et la complexité de la tâche.
        </p>
      ),
      key: '2',
      label: "C'est illimité ?",
    },
    {
      children: (
        <p>
          Oui, vos données sont hébergées en Algérie et conformes au RGPD. Vous pouvez aussi utiliser
          le mode local avec Ollama pour garder vos données entièrement sur votre machine.
        </p>
      ),
      key: '3',
      label: 'Mes données sont-elles privées ?',
    },
    {
      children: (
        <p>
          La plateforme supporte 3 langues : français, arabe et darija.
          L'arabe est également disponible. Les modèles IA peuvent générer du contenu dans plus de
          50 langues.
        </p>
      ),
      key: '4',
      label: 'Quelles langues sont supportées ?',
    },
    {
      children: (
        <p>
          Oui, vous pouvez arrêter à tout moment. Vos crédits restent valides et n'expirent pas.
          Aucun engagement, aucun abonnement obligatoire.
        </p>
      ),
      key: '5',
      label: 'Je peux annuler ?',
    },
  ];

  return (
    <div className={styles.page}>
      {/* HERO SECTION */}
      <section className={styles.hero}>
        <div className={styles.container}>
          <h1 className={styles.heroTitle}>
            La plateforme IA tout-en-un pour les entreprises et institutions algériennes
          </h1>
          <p className={styles.heroSubtitle}>
            Texte, Image, Vidéo, Audio, Code, Agents et Applications. Hébergement Algérie • Multilingue
            (FR/AR/Darija) • Conformité RGPD
          </p>
          <div className={styles.heroButtons}>
            <Button
              icon={<Icon icon={Rocket} />}
              onClick={() => handleNavigate('/signup')}
              size="large"
              type="primary"
            >
              Essayer gratuitement
            </Button>
            <Button onClick={() => handleNavigate('/profile/usage')} size="large">
              Voir les tarifs
            </Button>
          </div>
        </div>
      </section>

      {/* PROOF BAR */}
      <section className={styles.container}>
        <div className={styles.proofBar}>
          <div className={styles.proofItem}>
            <Icon icon={Layers} />
            <span>+30 modèles IA</span>
          </div>
          <div className={styles.proofItem}>
            <Icon icon={CreditCard} />
            <span>Paiement DZD</span>
          </div>
          <div className={styles.proofItem}>
            <Icon icon={Users} />
            <span>Support Algérie</span>
          </div>
          <div className={styles.proofItem}>
            <Icon icon={Lock} />
            <span>Hébergement Algérie</span>
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className={styles.section}>
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Comment ça marche</h2>
          <Flexbox gap={24} horizontal style={{ flexWrap: 'wrap' }}>
            <div className={styles.howCard}>
              <div className={styles.howNumber}>1</div>
              <h3 className={styles.howTitle}>Créez votre compte</h3>
              <p className={styles.howDescription}>
                Inscription gratuite en quelques secondes. Accès immédiat à la plateforme.
              </p>
            </div>
            <div className={styles.howCard}>
              <div className={styles.howNumber}>2</div>
              <h3 className={styles.howTitle}>Choisissez votre outil IA</h3>
              <p className={styles.howDescription}>
                Texte, image, audio, code... Sélectionnez l'outil adapté à votre besoin.
              </p>
            </div>
            <div className={styles.howCard}>
              <div className={styles.howNumber}>3</div>
              <h3 className={styles.howTitle}>Utilisez vos crédits</h3>
              <p className={styles.howDescription}>
                Payez uniquement ce que vous utilisez. Rechargez quand vous voulez.
              </p>
            </div>
          </Flexbox>
        </div>
      </section>

      {/* USE CASES - VERTICALS */}
      <section className={styles.section} style={{ background: 'transparent' }}>
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Solutions par secteur</h2>
          <Flexbox gap={24} horizontal style={{ flexWrap: 'wrap' }}>
            <div className={styles.useCaseCard} onClick={() => handleNavigate('/education')}>
              <div className={styles.useCaseIcon} style={{ background: '#05966915', color: '#059669' }}>
                <Icon icon={BookOpen} size={24} />
              </div>
              <h3 className={styles.useCaseTitle}>Education</h3>
              <p className={styles.useCaseDescription}>
                Tuteur IA pour élèves, aide aux devoirs, préparation examens, support enseignants.
              </p>
              <div className={styles.useCaseLink} style={{ color: '#059669' }}>
                Découvrir <Icon icon={ChevronRight} size={16} />
              </div>
            </div>
            <div className={styles.useCaseCard} onClick={() => handleNavigate('/business')}>
              <div className={styles.useCaseIcon} style={{ background: '#7c3aed15', color: '#7c3aed' }}>
                <Icon icon={BriefcaseBusiness} size={24} />
              </div>
              <h3 className={styles.useCaseTitle}>PME & Entreprises</h3>
              <p className={styles.useCaseDescription}>
                Automatisation administrative, emails, rapports, analyse de données.
              </p>
              <div className={styles.useCaseLink} style={{ color: '#7c3aed' }}>
                Découvrir <Icon icon={ChevronRight} size={16} />
              </div>
            </div>
            <div className={styles.useCaseCard} onClick={() => handleNavigate('/legal')}>
              <div className={styles.useCaseIcon} style={{ background: '#1a365d15', color: '#1a365d' }}>
                <Icon icon={FileText} size={24} />
              </div>
              <h3 className={styles.useCaseTitle}>Juridique</h3>
              <p className={styles.useCaseDescription}>
                Recherche légale, analyse de contrats, rédaction juridique, droit algérien.
              </p>
              <div className={styles.useCaseLink} style={{ color: '#1a365d' }}>
                Découvrir <Icon icon={ChevronRight} size={16} />
              </div>
            </div>
            <div className={styles.useCaseCard} onClick={() => handleNavigate('/image')}>
              <div className={styles.useCaseIcon}>
                <Icon icon={Palette} size={24} />
              </div>
              <h3 className={styles.useCaseTitle}>Création contenu</h3>
              <p className={styles.useCaseDescription}>
                Images, textes marketing, posts réseaux sociaux et visuels.
              </p>
              <div className={styles.useCaseLink}>
                Commencer <Icon icon={ChevronRight} size={16} />
              </div>
            </div>
          </Flexbox>
        </div>
      </section>

      {/* ALGERIA DIFFERENTIATION */}
      <section className={styles.section}>
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Pourquoi nous choisir en Algérie</h2>
          <Flexbox gap={24} horizontal style={{ flexWrap: 'wrap' }}>
            <div className={styles.diffBlock}>
              <div className={styles.diffIcon}>
                <Icon icon={CreditCard} size={28} />
              </div>
              <h3 className={styles.diffTitle}>Paiement en DZD</h3>
              <p className={styles.diffDescription}>
                Facturation en dinars algériens, TVA incluse. Paiement par carte, virement IBAN ou
                facture pour les entreprises.
              </p>
            </div>
            <div className={styles.diffBlock}>
              <div className={styles.diffIcon}>
                <Icon icon={Sparkles} size={28} />
              </div>
              <h3 className={styles.diffTitle}>Tous les modèles au même endroit</h3>
              <p className={styles.diffDescription}>
                GPT-4, Claude, Gemini, Mistral, Llama et plus. Un seul compte pour accéder aux
                meilleurs modèles IA du monde.
              </p>
            </div>
            <div className={styles.diffBlock}>
              <div className={styles.diffIcon}>
                <Icon icon={Server} size={28} />
              </div>
              <h3 className={styles.diffTitle}>Hébergement Algérie</h3>
              <p className={styles.diffDescription}>
                Données hébergées en Algérie, conformité RGPD. Option 100% local avec Ollama pour une
                confidentialité totale.
              </p>
            </div>
          </Flexbox>
        </div>
      </section>

      {/* CREDITS BLOCK */}
      <section className={styles.section}>
        <div className={styles.container}>
          <div className={styles.creditsBlock}>
            <Flexbox align="center" gap={8} horizontal justify="center" style={{ marginBottom: 16 }}>
              <Icon icon={Zap} size={32} />
            </Flexbox>
            <h2 className={styles.creditsTitle}>Système de crédits simple</h2>
            <p className={styles.creditsDescription}>
              Achetez des crédits une fois, utilisez-les quand vous voulez. Chaque action IA
              consomme un nombre de crédits selon le modèle utilisé. Pas d'abonnement, pas
              d'engagement. Vos crédits n'expirent jamais.
            </p>
            <Button
              icon={<Icon icon={CreditCard} />}
              onClick={() => handleNavigate('/profile/usage')}
              size="large"
              type="primary"
            >
              Voir les tarifs
            </Button>
          </div>
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
            <h2 className={styles.ctaFinalTitle}>Commencez maintenant</h2>
            <p className={styles.ctaFinalSubtitle}>
              Découvrez ce que l'IA peut faire pour votre organisation en Algérie.
            </p>
            <Button
              icon={<Icon icon={Check} />}
              onClick={() => handleNavigate('/signup')}
              size="large"
              style={{
                background: '#fff',
                borderColor: '#fff',
                color: '#1677ff',
              }}
            >
              Créer un compte gratuit
            </Button>
          </div>
        </div>
      </section>

      {/* FOOTER SPACING */}
      <Center padding={40}>
        <Flexbox align="center" gap={16}>
          <Flexbox gap={8} horizontal style={{ color: 'rgba(0,0,0,0.45)', fontSize: 14 }}>
            <Globe size={16} />
            <span>IAFactory Algeria - Plateforme IA pour les entreprises algériennes</span>
          </Flexbox>
        </Flexbox>
      </Center>
    </div>
  );
});

LandingPage.displayName = 'LandingPage';

export default LandingPage;
