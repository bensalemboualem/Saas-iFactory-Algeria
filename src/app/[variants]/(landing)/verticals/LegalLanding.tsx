'use client';

import { Button, Icon } from '@lobehub/ui';
import { Collapse, CollapseProps } from 'antd';
import { createStyles } from 'antd-style';
import {
  BookOpen,
  Check,
  ChevronRight,
  CreditCard,
  FileSearch,
  Gavel,
  Globe,
  Layers,
  Lock,
  Scale,
  ScrollText,
  Server,
  Shield,
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
    background: linear-gradient(135deg, #1a365d 0%, #2d5a87 100%);
    border-radius: ${token.borderRadius}px;
    color: #fff;
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
  ctaFinal: css`
    padding: 60px 40px;
    text-align: center;
    background: linear-gradient(135deg, #1a365d 0%, #2d5a87 100%);
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
    background: linear-gradient(135deg, #1a365d20 0%, #2d5a8720 100%);
    border-radius: 50%;
    color: #1a365d;
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
    background: linear-gradient(180deg, #1a365d08 0%, transparent 100%);
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
    color: #1a365d;
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
    color: #1a365d;
    background: #1a365d15;
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
  tag: css`
    display: inline-block;
    padding: 4px 12px;
    margin-bottom: 16px;
    font-size: 12px;
    font-weight: 600;
    color: #1a365d;
    text-transform: uppercase;
    letter-spacing: 1px;
    background: #1a365d15;
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
      border-color: #1a365d;
      box-shadow: 0 4px 16px #1a365d15;
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
    background: #1a365d15;
    border-radius: ${token.borderRadius}px;
    color: #1a365d;
  `,
  useCaseLink: css`
    display: flex;
    gap: 4px;
    align-items: center;
    font-size: 14px;
    font-weight: 500;
    color: #1a365d;
  `,
  useCaseTitle: css`
    margin: 0 0 8px;
    font-size: 18px;
    font-weight: 600;
    color: ${token.colorText};
  `,
}));

const LegalLanding = memo(() => {
  const { styles } = useStyles();
  const navigate = useNavigate();

  const handleNavigate = (path: string) => {
    navigate(path);
  };

  const faqItems: CollapseProps['items'] = [
    {
      children: (
        <p>
          Oui, nos assistants IA sont entraînés sur le droit algérien (Code civil, Code du
          Commerce, Code du Travail, etc.) et peuvent vous aider à analyser des documents juridiques,
          rédiger des contrats, et effectuer des recherches légales.
        </p>
      ),
      key: '1',
      label: 'Les assistants connaissent-ils le droit algérien ?',
    },
    {
      children: (
        <p>
          Absolument. Vous pouvez choisir le mode 100% local avec Ollama pour que vos documents
          confidentiels ne quittent jamais votre infrastructure. Aucune donnée n'est envoyée sur
          internet.
        </p>
      ),
      key: '2',
      label: 'Mes documents confidentiels sont-ils sécurisés ?',
    },
    {
      children: (
        <p>
          Non, IAFactory Legal est un outil d'assistance. Il aide à la recherche, à l'analyse et à
          la rédaction, mais ne remplace pas le conseil d'un avocat qualifié. C'est un assistant,
          pas un conseiller juridique.
        </p>
      ),
      key: '3',
      label: 'IAFactory peut-il remplacer un avocat ?',
    },
    {
      children: (
        <p>
          Français, arabe et darija - les langues utilisées en Algérie plus
          l'anglais pour les affaires internationales.
        </p>
      ),
      key: '4',
      label: 'En quelles langues puis-je travailler ?',
    },
    {
      children: (
        <p>
          Oui, vous pouvez créer des bases de connaissances personnalisées avec vos propres
          documents, jurisprudence et modèles de contrats pour des réponses encore plus précises.
        </p>
      ),
      key: '5',
      label: 'Puis-je ajouter ma propre documentation juridique ?',
    },
  ];

  return (
    <div className={styles.page}>
      {/* HERO SECTION */}
      <section className={styles.hero}>
        <div className={styles.container}>
          <span className={styles.tag}>Juridique & Legal Tech</span>
          <h1 className={styles.heroTitle}>
            L'IA au service des professionnels du droit en Algérie
          </h1>
          <p className={styles.heroSubtitle}>
            Recherche juridique, analyse de documents, rédaction de contrats. Gagnez du temps sur
            les tâches répétitives et concentrez-vous sur le conseil à valeur ajoutée.
          </p>
          <div className={styles.heroButtons}>
            <Button
              icon={<Icon icon={Scale} />}
              onClick={() => handleNavigate('/signup')}
              size="large"
              style={{ background: '#1a365d', borderColor: '#1a365d' }}
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
            <Icon icon={Shield} />
            <span>Confidentialité garantie</span>
          </div>
          <div className={styles.proofItem}>
            <Icon icon={Globe} />
            <span>Droit algérien intégré</span>
          </div>
          <div className={styles.proofItem}>
            <Icon icon={Layers} />
            <span>Multi-modèles IA</span>
          </div>
          <div className={styles.proofItem}>
            <Icon icon={Lock} />
            <span>Mode 100% local</span>
          </div>
        </div>
      </section>

      {/* USE CASES */}
      <section className={styles.section}>
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Ce que vous pouvez faire</h2>
          <Flexbox gap={24} horizontal style={{ flexWrap: 'wrap' }}>
            <div className={styles.useCaseCard} onClick={() => handleNavigate('/chat')}>
              <div className={styles.useCaseIcon}>
                <Icon icon={FileSearch} size={24} />
              </div>
              <h3 className={styles.useCaseTitle}>Recherche juridique</h3>
              <p className={styles.useCaseDescription}>
                Trouvez rapidement la jurisprudence et les articles de loi pertinents.
              </p>
              <div className={styles.useCaseLink}>
                Commencer <Icon icon={ChevronRight} size={16} />
              </div>
            </div>
            <div className={styles.useCaseCard} onClick={() => handleNavigate('/chat')}>
              <div className={styles.useCaseIcon}>
                <Icon icon={ScrollText} size={24} />
              </div>
              <h3 className={styles.useCaseTitle}>Analyse de contrats</h3>
              <p className={styles.useCaseDescription}>
                Analysez des contrats et identifiez les clauses importantes ou risquées.
              </p>
              <div className={styles.useCaseLink}>
                Commencer <Icon icon={ChevronRight} size={16} />
              </div>
            </div>
            <div className={styles.useCaseCard} onClick={() => handleNavigate('/chat')}>
              <div className={styles.useCaseIcon}>
                <Icon icon={Gavel} size={24} />
              </div>
              <h3 className={styles.useCaseTitle}>Rédaction juridique</h3>
              <p className={styles.useCaseDescription}>
                Générez des ébauches de contrats, lettres et documents légaux.
              </p>
              <div className={styles.useCaseLink}>
                Commencer <Icon icon={ChevronRight} size={16} />
              </div>
            </div>
            <div className={styles.useCaseCard} onClick={() => handleNavigate('/knowledge')}>
              <div className={styles.useCaseIcon}>
                <Icon icon={BookOpen} size={24} />
              </div>
              <h3 className={styles.useCaseTitle}>Base documentaire</h3>
              <p className={styles.useCaseDescription}>
                Créez votre propre base de connaissances juridiques privée.
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
          <h2 className={styles.sectionTitle}>Pourquoi les juristes nous choisissent</h2>
          <Flexbox gap={24} horizontal style={{ flexWrap: 'wrap' }}>
            <div className={styles.diffBlock}>
              <div className={styles.diffIcon}>
                <Icon icon={Shield} size={28} />
              </div>
              <h3 className={styles.diffTitle}>Secret professionnel respecté</h3>
              <p className={styles.diffDescription}>
                Mode local disponible pour que vos documents confidentiels restent sur votre
                infrastructure. Conformité avec les règles déontologiques.
              </p>
            </div>
            <div className={styles.diffBlock}>
              <div className={styles.diffIcon}>
                <Icon icon={Sparkles} size={28} />
              </div>
              <h3 className={styles.diffTitle}>IA de pointe</h3>
              <p className={styles.diffDescription}>
                Accès aux meilleurs modèles (GPT-4, Claude, Gemini) optimisés pour le traitement de
                textes juridiques complexes.
              </p>
            </div>
            <div className={styles.diffBlock}>
              <div className={styles.diffIcon}>
                <Icon icon={Server} size={28} />
              </div>
              <h3 className={styles.diffTitle}>Hébergement Algérie</h3>
              <p className={styles.diffDescription}>
                Vos données sont hébergées en Algérie, conformément aux exigences de protection des
                données les plus strictes.
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
            <h2 className={styles.ctaFinalTitle}>Transformez votre pratique juridique</h2>
            <p className={styles.ctaFinalSubtitle}>
              Rejoignez les cabinets qui utilisent déjà l'IA pour gagner en efficacité.
            </p>
            <Button
              icon={<Icon icon={Check} />}
              onClick={() => handleNavigate('/signup')}
              size="large"
              style={{
                background: '#fff',
                borderColor: '#fff',
                color: '#1a365d',
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
            <Scale size={16} />
            <span>IAFactory Legal - Solution IA pour les professionnels du droit</span>
          </Flexbox>
        </Flexbox>
      </Center>
    </div>
  );
});

LegalLanding.displayName = 'LegalLanding';

export default LegalLanding;
