'use client';

import { Button, Icon } from '@lobehub/ui';
import { Collapse, CollapseProps } from 'antd';
import { createStyles } from 'antd-style';
import {
  BookOpen,
  BrainCircuit,
  Check,
  ChevronRight,
  FileText,
  GraduationCap,
  Languages,
  Layers,
  Lock,
  PenTool,
  School,
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
    background: linear-gradient(135deg, #059669 0%, #10b981 100%);
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
    background: linear-gradient(135deg, #05966920 0%, #10b98120 100%);
    border-radius: 50%;
    color: #059669;
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
    background: linear-gradient(180deg, #05966908 0%, transparent 100%);
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
    color: #059669;
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
    color: #059669;
    text-transform: uppercase;
    letter-spacing: 1px;
    background: #05966915;
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
      border-color: #059669;
      box-shadow: 0 4px 16px #05966915;
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
    background: #05966915;
    border-radius: ${token.borderRadius}px;
    color: #059669;
  `,
  useCaseLink: css`
    display: flex;
    gap: 4px;
    align-items: center;
    font-size: 14px;
    font-weight: 500;
    color: #059669;
  `,
  useCaseTitle: css`
    margin: 0 0 8px;
    font-size: 18px;
    font-weight: 600;
    color: ${token.colorText};
  `,
}));

const EducationLanding = memo(() => {
  const { styles } = useStyles();
  const navigate = useNavigate();

  const handleNavigate = (path: string) => {
    navigate(path);
  };

  const faqItems: CollapseProps['items'] = [
    {
      children: (
        <p>
          Oui, IAFactory Education propose des tarifs spéciaux pour les établissements scolaires,
          universités et hautes écoles. Contactez-nous pour un devis personnalisé avec gestion
          multi-utilisateurs.
        </p>
      ),
      key: '1',
      label: 'Y a-t-il des tarifs pour les écoles ?',
    },
    {
      children: (
        <p>
          Non, l'IA est un outil d'apprentissage. Elle explique, aide à comprendre et propose des
          exercices. Elle ne fait pas les devoirs à la place de l'élève, mais l'accompagne dans sa
          compréhension.
        </p>
      ),
      key: '2',
      label: "L'IA fait-elle les devoirs à la place des élèves ?",
    },
    {
      children: (
        <p>
          Français, arabe et darija. Les explications peuvent être dans une langue et le contenu
          étudié dans une autre - parfait pour l'apprentissage multilingue.
        </p>
      ),
      key: '3',
      label: 'Quelles langues sont disponibles ?',
    },
    {
      children: (
        <p>
          Oui, les enseignants peuvent créer des bases de connaissances avec leurs propres cours,
          exercices et supports pédagogiques pour des réponses adaptées à leur programme.
        </p>
      ),
      key: '4',
      label: 'Les enseignants peuvent-ils personnaliser les contenus ?',
    },
    {
      children: (
        <p>
          Absolument. La protection des données des mineurs est une priorité. Aucune donnée
          personnelle n'est utilisée pour l'entraînement des modèles, et le mode local est
          disponible.
        </p>
      ),
      key: '5',
      label: 'Les données des élèves sont-elles protégées ?',
    },
  ];

  return (
    <div className={styles.page}>
      {/* HERO SECTION */}
      <section className={styles.hero}>
        <div className={styles.container}>
          <span className={styles.tag}>Education & Formation</span>
          <h1 className={styles.heroTitle}>L'IA comme tuteur personnel pour chaque élève</h1>
          <p className={styles.heroSubtitle}>
            Explications personnalisées, aide aux devoirs, préparation aux examens. Un assistant
            pédagogique disponible 24h/24 en français, arabe et darija.
          </p>
          <div className={styles.heroButtons}>
            <Button
              icon={<Icon icon={GraduationCap} />}
              onClick={() => handleNavigate('/signup')}
              size="large"
              style={{ background: '#059669', borderColor: '#059669' }}
              type="primary"
            >
              Essayer gratuitement
            </Button>
            <Button onClick={() => handleNavigate('/profile/usage')} size="large">
              Tarifs écoles
            </Button>
          </div>
        </div>
      </section>

      {/* PROOF BAR */}
      <section className={styles.container}>
        <div className={styles.proofBar}>
          <div className={styles.proofItem}>
            <Icon icon={Languages} />
            <span>3 langues (FR/AR/Darija)</span>
          </div>
          <div className={styles.proofItem}>
            <Icon icon={School} />
            <span>Tous niveaux scolaires</span>
          </div>
          <div className={styles.proofItem}>
            <Icon icon={Layers} />
            <span>Toutes matières</span>
          </div>
          <div className={styles.proofItem}>
            <Icon icon={Lock} />
            <span>Données protégées</span>
          </div>
        </div>
      </section>

      {/* USE CASES */}
      <section className={styles.section}>
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Comment IAFactory aide à apprendre</h2>
          <Flexbox gap={24} horizontal style={{ flexWrap: 'wrap' }}>
            <div className={styles.useCaseCard} onClick={() => handleNavigate('/chat')}>
              <div className={styles.useCaseIcon}>
                <Icon icon={BrainCircuit} size={24} />
              </div>
              <h3 className={styles.useCaseTitle}>Explications personnalisées</h3>
              <p className={styles.useCaseDescription}>
                L'IA adapte ses explications au niveau et au style d'apprentissage de chaque élève.
              </p>
              <div className={styles.useCaseLink}>
                Commencer <Icon icon={ChevronRight} size={16} />
              </div>
            </div>
            <div className={styles.useCaseCard} onClick={() => handleNavigate('/chat')}>
              <div className={styles.useCaseIcon}>
                <Icon icon={PenTool} size={24} />
              </div>
              <h3 className={styles.useCaseTitle}>Aide aux devoirs</h3>
              <p className={styles.useCaseDescription}>
                Guidance pas à pas pour comprendre et résoudre les exercices par soi-même.
              </p>
              <div className={styles.useCaseLink}>
                Commencer <Icon icon={ChevronRight} size={16} />
              </div>
            </div>
            <div className={styles.useCaseCard} onClick={() => handleNavigate('/chat')}>
              <div className={styles.useCaseIcon}>
                <Icon icon={FileText} size={24} />
              </div>
              <h3 className={styles.useCaseTitle}>Préparation examens</h3>
              <p className={styles.useCaseDescription}>
                Résumés, quiz personnalisés et révisions adaptées pour chaque matière.
              </p>
              <div className={styles.useCaseLink}>
                Commencer <Icon icon={ChevronRight} size={16} />
              </div>
            </div>
            <div className={styles.useCaseCard} onClick={() => handleNavigate('/knowledge')}>
              <div className={styles.useCaseIcon}>
                <Icon icon={BookOpen} size={24} />
              </div>
              <h3 className={styles.useCaseTitle}>Cours personnalisés</h3>
              <p className={styles.useCaseDescription}>
                Les enseignants créent des assistants avec leurs propres supports de cours.
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
          <h2 className={styles.sectionTitle}>Conçu pour l'éducation algérienne</h2>
          <Flexbox gap={24} horizontal style={{ flexWrap: 'wrap' }}>
            <div className={styles.diffBlock}>
              <div className={styles.diffIcon}>
                <Icon icon={Languages} size={28} />
              </div>
              <h3 className={styles.diffTitle}>Multilingue natif</h3>
              <p className={styles.diffDescription}>
                Travaillez en français, arabe ou darija. Parfait pour les élèves algériens et
                l'apprentissage multilingue.
              </p>
            </div>
            <div className={styles.diffBlock}>
              <div className={styles.diffIcon}>
                <Icon icon={Users} size={28} />
              </div>
              <h3 className={styles.diffTitle}>Gestion de classe</h3>
              <p className={styles.diffDescription}>
                Les enseignants peuvent créer des groupes, suivre l'utilisation et personnaliser les
                assistants pour leur classe.
              </p>
            </div>
            <div className={styles.diffBlock}>
              <div className={styles.diffIcon}>
                <Icon icon={Sparkles} size={28} />
              </div>
              <h3 className={styles.diffTitle}>Pédagogie adaptative</h3>
              <p className={styles.diffDescription}>
                L'IA identifie les lacunes et propose des exercices ciblés pour progresser
                efficacement.
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
            <h2 className={styles.ctaFinalTitle}>Donnez à chaque élève un tuteur IA</h2>
            <p className={styles.ctaFinalSubtitle}>
              Testez gratuitement et découvrez comment l'IA peut transformer l'apprentissage.
            </p>
            <Button
              icon={<Icon icon={Check} />}
              onClick={() => handleNavigate('/signup')}
              size="large"
              style={{
                background: '#fff',
                borderColor: '#fff',
                color: '#059669',
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
            <GraduationCap size={16} />
            <span>IAFactory Education - L'IA au service de l'apprentissage</span>
          </Flexbox>
        </Flexbox>
      </Center>
    </div>
  );
});

EducationLanding.displayName = 'EducationLanding';

export default EducationLanding;
