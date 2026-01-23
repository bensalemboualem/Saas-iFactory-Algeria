export interface MathFormula {
  id: string;
  name: string;
  formula: string;
  description: string;
  category: 'geometrie' | 'algebre' | 'analyse' | 'trigonometrie';
  level: 'college' | 'lycee' | 'universite';
}

export const FORMULAS: MathFormula[] = [
  // Géométrie - Collège
  {
    id: 'aire-carre',
    name: 'Aire du carré',
    formula: 'A = c²',
    description: 'c = côté',
    category: 'geometrie',
    level: 'college',
  },
  {
    id: 'aire-rectangle',
    name: 'Aire du rectangle',
    formula: 'A = L × l',
    description: 'L = longueur, l = largeur',
    category: 'geometrie',
    level: 'college',
  },
  {
    id: 'aire-triangle',
    name: 'Aire du triangle',
    formula: 'A = (b × h) / 2',
    description: 'b = base, h = hauteur perpendiculaire',
    category: 'geometrie',
    level: 'college',
  },
  {
    id: 'aire-cercle',
    name: 'Aire du cercle',
    formula: 'A = πr²',
    description: 'r = rayon, π ≈ 3.14',
    category: 'geometrie',
    level: 'college',
  },
  {
    id: 'perimetre-cercle',
    name: 'Périmètre du cercle',
    formula: 'P = 2πr',
    description: 'r = rayon',
    category: 'geometrie',
    level: 'college',
  },
  {
    id: 'volume-cube',
    name: 'Volume du cube',
    formula: 'V = c³',
    description: 'c = côté',
    category: 'geometrie',
    level: 'college',
  },
  {
    id: 'volume-pave',
    name: 'Volume du pavé',
    formula: 'V = L × l × h',
    description: 'L = longueur, l = largeur, h = hauteur',
    category: 'geometrie',
    level: 'college',
  },
  {
    id: 'volume-cylindre',
    name: 'Volume du cylindre',
    formula: 'V = πr²h',
    description: 'r = rayon de la base, h = hauteur',
    category: 'geometrie',
    level: 'college',
  },
  {
    id: 'volume-sphere',
    name: 'Volume de la sphère',
    formula: 'V = (4/3)πr³',
    description: 'r = rayon',
    category: 'geometrie',
    level: 'lycee',
  },
  {
    id: 'pythagore',
    name: 'Théorème de Pythagore',
    formula: 'a² + b² = c²',
    description: 'Triangle rectangle: c = hypoténuse',
    category: 'geometrie',
    level: 'college',
  },
  {
    id: 'thales',
    name: 'Théorème de Thalès',
    formula: 'AB/AB\' = AC/AC\' = BC/B\'C\'',
    description: 'Droites parallèles coupant 2 sécantes',
    category: 'geometrie',
    level: 'college',
  },

  // Algèbre
  {
    id: 'identite-1',
    name: 'Identité remarquable (a+b)²',
    formula: '(a + b)² = a² + 2ab + b²',
    description: 'Carré d\'une somme',
    category: 'algebre',
    level: 'college',
  },
  {
    id: 'identite-2',
    name: 'Identité remarquable (a-b)²',
    formula: '(a - b)² = a² - 2ab + b²',
    description: 'Carré d\'une différence',
    category: 'algebre',
    level: 'college',
  },
  {
    id: 'identite-3',
    name: 'Identité remarquable a²-b²',
    formula: 'a² - b² = (a - b)(a + b)',
    description: 'Différence de deux carrés',
    category: 'algebre',
    level: 'college',
  },
  {
    id: 'equation-2nd-degre',
    name: 'Équation du 2nd degré',
    formula: 'x = (-b ± √Δ) / 2a',
    description: 'ax² + bx + c = 0, Δ = b² - 4ac',
    category: 'algebre',
    level: 'lycee',
  },
  {
    id: 'discriminant',
    name: 'Discriminant Δ',
    formula: 'Δ = b² - 4ac',
    description: 'Si Δ>0: 2 solutions, Δ=0: 1 solution, Δ<0: pas de solution réelle',
    category: 'algebre',
    level: 'lycee',
  },

  // Analyse - Dérivées
  {
    id: 'derivee-puissance',
    name: 'Dérivée de xⁿ',
    formula: '(xⁿ)\' = n × xⁿ⁻¹',
    description: 'n ∈ ℝ',
    category: 'analyse',
    level: 'lycee',
  },
  {
    id: 'derivee-exp',
    name: 'Dérivée de eˣ',
    formula: '(eˣ)\' = eˣ',
    description: 'La fonction exponentielle est sa propre dérivée',
    category: 'analyse',
    level: 'lycee',
  },
  {
    id: 'derivee-ln',
    name: 'Dérivée de ln(x)',
    formula: '(ln x)\' = 1/x',
    description: 'x > 0',
    category: 'analyse',
    level: 'lycee',
  },
  {
    id: 'derivee-sin',
    name: 'Dérivée de sin(x)',
    formula: '(sin x)\' = cos x',
    description: '',
    category: 'analyse',
    level: 'lycee',
  },
  {
    id: 'derivee-cos',
    name: 'Dérivée de cos(x)',
    formula: '(cos x)\' = -sin x',
    description: 'Attention au signe moins!',
    category: 'analyse',
    level: 'lycee',
  },

  // Analyse - Primitives
  {
    id: 'primitive-puissance',
    name: 'Primitive de xⁿ',
    formula: '∫ xⁿ dx = xⁿ⁺¹/(n+1) + C',
    description: 'n ≠ -1, C = constante',
    category: 'analyse',
    level: 'lycee',
  },
  {
    id: 'primitive-inverse',
    name: 'Primitive de 1/x',
    formula: '∫ (1/x) dx = ln|x| + C',
    description: 'x ≠ 0',
    category: 'analyse',
    level: 'lycee',
  },
  {
    id: 'primitive-exp',
    name: 'Primitive de eˣ',
    formula: '∫ eˣ dx = eˣ + C',
    description: '',
    category: 'analyse',
    level: 'lycee',
  },

  // Trigonométrie
  {
    id: 'pythagore-trigo',
    name: 'Relation fondamentale',
    formula: 'cos²(x) + sin²(x) = 1',
    description: 'Pour tout angle x',
    category: 'trigonometrie',
    level: 'lycee',
  },
  {
    id: 'tan',
    name: 'Tangente',
    formula: 'tan(x) = sin(x) / cos(x)',
    description: 'cos(x) ≠ 0',
    category: 'trigonometrie',
    level: 'lycee',
  },
  {
    id: 'soh-cah-toa',
    name: 'SOH-CAH-TOA',
    formula: 'sin = Opposé/Hypoténuse, cos = Adjacent/Hypoténuse, tan = Opposé/Adjacent',
    description: 'Triangle rectangle uniquement',
    category: 'trigonometrie',
    level: 'college',
  },
];
