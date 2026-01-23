// CAN 2025 - Coupe d'Afrique des Nations au Maroc
// 21 décembre 2025 - 18 janvier 2026

export interface Team {
  id: string;
  name: string;
  nameFr: string;
  nameAr: string;
  flag: string;
  group: string;
  fifa_rank?: number;
}

export interface Match {
  id: string;
  date: string; // ISO format
  time: string;
  homeTeam: string;
  awayTeam: string;
  stadium: string;
  city: string;
  group?: string;
  stage: 'group' | 'round16' | 'quarter' | 'semi' | 'final';
  homeScore?: number;
  awayScore?: number;
}

export interface Group {
  name: string;
  teams: string[]; // team IDs
}

// 24 équipes qualifiées
export const TEAMS: Team[] = [
  // Groupe A
  { id: 'MAR', name: 'Morocco', nameFr: 'Maroc', nameAr: 'المغرب', flag: '🇲🇦', group: 'A' },
  { id: 'MLI', name: 'Mali', nameFr: 'Mali', nameAr: 'مالي', flag: '🇲🇱', group: 'A' },
  { id: 'ZIM', name: 'Zimbabwe', nameFr: 'Zimbabwe', nameAr: 'زيمبابوي', flag: '🇿🇼', group: 'A' },
  { id: 'COM', name: 'Comoros', nameFr: 'Comores', nameAr: 'جزر القمر', flag: '🇰🇲', group: 'A' },

  // Groupe B
  { id: 'EGY', name: 'Egypt', nameFr: 'Égypte', nameAr: 'مصر', flag: '🇪🇬', group: 'B' },
  { id: 'GAB', name: 'Gabon', nameFr: 'Gabon', nameAr: 'الغابون', flag: '🇬🇦', group: 'B' },
  { id: 'TAN', name: 'Tanzania', nameFr: 'Tanzanie', nameAr: 'تنزانيا', flag: '🇹🇿', group: 'B' },
  { id: 'MOZ', name: 'Mozambique', nameFr: 'Mozambique', nameAr: 'موزمبيق', flag: '🇲🇿', group: 'B' },

  // Groupe C
  { id: 'SEN', name: 'Senegal', nameFr: 'Sénégal', nameAr: 'السنغال', flag: '🇸🇳', group: 'C' },
  { id: 'CIV', name: 'Ivory Coast', nameFr: 'Côte d\'Ivoire', nameAr: 'ساحل العاج', flag: '🇨🇮', group: 'C' },
  { id: 'UGA', name: 'Uganda', nameFr: 'Ouganda', nameAr: 'أوغندا', flag: '🇺🇬', group: 'C' },
  { id: 'BEN', name: 'Benin', nameFr: 'Bénin', nameAr: 'بنين', flag: '🇧🇯', group: 'C' },

  // Groupe D
  { id: 'NGA', name: 'Nigeria', nameFr: 'Nigeria', nameAr: 'نيجيريا', flag: '🇳🇬', group: 'D' },
  { id: 'CMR', name: 'Cameroon', nameFr: 'Cameroun', nameAr: 'الكاميرون', flag: '🇨🇲', group: 'D' },
  { id: 'ANG', name: 'Angola', nameFr: 'Angola', nameAr: 'أنغولا', flag: '🇦🇴', group: 'D' },
  { id: 'NAM', name: 'Namibia', nameFr: 'Namibie', nameAr: 'ناميبيا', flag: '🇳🇦', group: 'D' },

  // Groupe E - ALGÉRIE 🇩🇿
  { id: 'ALG', name: 'Algeria', nameFr: 'Algérie', nameAr: 'الجزائر', flag: '🇩🇿', group: 'E', fifa_rank: 37 },
  { id: 'BFA', name: 'Burkina Faso', nameFr: 'Burkina Faso', nameAr: 'بوركينا فاسو', flag: '🇧🇫', group: 'E' },
  { id: 'EQG', name: 'Eq. Guinea', nameFr: 'Guinée équatoriale', nameAr: 'غينيا الاستوائية', flag: '🇬🇶', group: 'E' },
  { id: 'SUD', name: 'Sudan', nameFr: 'Soudan', nameAr: 'السودان', flag: '🇸🇩', group: 'E' },

  // Groupe F
  { id: 'TUN', name: 'Tunisia', nameFr: 'Tunisie', nameAr: 'تونس', flag: '🇹🇳', group: 'F' },
  { id: 'RSA', name: 'South Africa', nameFr: 'Afrique du Sud', nameAr: 'جنوب أفريقيا', flag: '🇿🇦', group: 'F' },
  { id: 'ZAM', name: 'Zambia', nameFr: 'Zambie', nameAr: 'زامبيا', flag: '🇿🇲', group: 'F' },
  { id: 'BOT', name: 'Botswana', nameFr: 'Botswana', nameAr: 'بوتسوانا', flag: '🇧🇼', group: 'F' },
];

export const GROUPS: Group[] = [
  { name: 'A', teams: ['MAR', 'MLI', 'ZIM', 'COM'] },
  { name: 'B', teams: ['EGY', 'GAB', 'TAN', 'MOZ'] },
  { name: 'C', teams: ['SEN', 'CIV', 'UGA', 'BEN'] },
  { name: 'D', teams: ['NGA', 'CMR', 'ANG', 'NAM'] },
  { name: 'E', teams: ['ALG', 'BFA', 'EQG', 'SUD'] },
  { name: 'F', teams: ['TUN', 'RSA', 'ZAM', 'BOT'] },
];

// Matchs de l'Algérie (Groupe E)
export const ALGERIA_MATCHES: Match[] = [
  {
    id: 'alg-1',
    date: '2025-12-24',
    time: '17:00',
    homeTeam: 'ALG',
    awayTeam: 'EQG',
    stadium: 'Stade Prince Moulay Abdellah',
    city: 'Rabat',
    group: 'E',
    stage: 'group',
  },
  {
    id: 'alg-2',
    date: '2025-12-28',
    time: '20:00',
    homeTeam: 'ALG',
    awayTeam: 'BFA',
    stadium: 'Stade Prince Moulay Abdellah',
    city: 'Rabat',
    group: 'E',
    stage: 'group',
  },
  {
    id: 'alg-3',
    date: '2025-12-31',
    time: '20:00',
    homeTeam: 'ALG',
    awayTeam: 'SUD',
    stadium: 'Stade Prince Moulay Abdellah',
    city: 'Rabat',
    group: 'E',
    stage: 'group',
  },
];

// Calendrier complet (phase de groupes - premiers matchs)
export const ALL_MATCHES: Match[] = [
  // Jour 1 - 21 décembre 2025
  {
    id: 'm1',
    date: '2025-12-21',
    time: '18:00',
    homeTeam: 'MAR',
    awayTeam: 'COM',
    stadium: 'Stade Mohammed V',
    city: 'Casablanca',
    group: 'A',
    stage: 'group',
  },
  {
    id: 'm2',
    date: '2025-12-21',
    time: '21:00',
    homeTeam: 'MLI',
    awayTeam: 'ZIM',
    stadium: 'Stade Mohammed V',
    city: 'Casablanca',
    group: 'A',
    stage: 'group',
  },

  // Jour 2 - 22 décembre 2025
  {
    id: 'm3',
    date: '2025-12-22',
    time: '17:00',
    homeTeam: 'EGY',
    awayTeam: 'MOZ',
    stadium: 'Stade Adrar',
    city: 'Agadir',
    group: 'B',
    stage: 'group',
  },
  {
    id: 'm4',
    date: '2025-12-22',
    time: '20:00',
    homeTeam: 'GAB',
    awayTeam: 'TAN',
    stadium: 'Stade Adrar',
    city: 'Agadir',
    group: 'B',
    stage: 'group',
  },

  // Jour 3 - 23 décembre 2025
  {
    id: 'm5',
    date: '2025-12-23',
    time: '17:00',
    homeTeam: 'SEN',
    awayTeam: 'BEN',
    stadium: 'Stade Grand Stade de Marrakech',
    city: 'Marrakech',
    group: 'C',
    stage: 'group',
  },
  {
    id: 'm6',
    date: '2025-12-23',
    time: '20:00',
    homeTeam: 'CIV',
    awayTeam: 'UGA',
    stadium: 'Stade Grand Stade de Marrakech',
    city: 'Marrakech',
    group: 'C',
    stage: 'group',
  },

  // Jour 4 - 24 décembre 2025 - ALGÉRIE! 🇩🇿
  {
    id: 'm7',
    date: '2025-12-24',
    time: '17:00',
    homeTeam: 'ALG',
    awayTeam: 'EQG',
    stadium: 'Stade Prince Moulay Abdellah',
    city: 'Rabat',
    group: 'E',
    stage: 'group',
  },
  {
    id: 'm8',
    date: '2025-12-24',
    time: '20:00',
    homeTeam: 'BFA',
    awayTeam: 'SUD',
    stadium: 'Stade Prince Moulay Abdellah',
    city: 'Rabat',
    group: 'E',
    stage: 'group',
  },

  // Jour 5 - 25 décembre 2025
  {
    id: 'm9',
    date: '2025-12-25',
    time: '17:00',
    homeTeam: 'NGA',
    awayTeam: 'NAM',
    stadium: 'Stade de Fès',
    city: 'Fès',
    group: 'D',
    stage: 'group',
  },
  {
    id: 'm10',
    date: '2025-12-25',
    time: '20:00',
    homeTeam: 'CMR',
    awayTeam: 'ANG',
    stadium: 'Stade de Fès',
    city: 'Fès',
    group: 'D',
    stage: 'group',
  },

  // Jour 6 - 26 décembre 2025
  {
    id: 'm11',
    date: '2025-12-26',
    time: '17:00',
    homeTeam: 'TUN',
    awayTeam: 'BOT',
    stadium: 'Stade de Tanger',
    city: 'Tanger',
    group: 'F',
    stage: 'group',
  },
  {
    id: 'm12',
    date: '2025-12-26',
    time: '20:00',
    homeTeam: 'RSA',
    awayTeam: 'ZAM',
    stadium: 'Stade de Tanger',
    city: 'Tanger',
    group: 'F',
    stage: 'group',
  },

  // J2 - 28 décembre 2025 - ALGÉRIE vs BURKINA FASO! 🇩🇿
  {
    id: 'alg-2',
    date: '2025-12-28',
    time: '20:00',
    homeTeam: 'ALG',
    awayTeam: 'BFA',
    stadium: 'Stade Prince Moulay Abdellah',
    city: 'Rabat',
    group: 'E',
    stage: 'group',
  },

  // J3 - 31 décembre 2025 - ALGÉRIE vs SOUDAN! 🇩🇿
  {
    id: 'alg-3',
    date: '2025-12-31',
    time: '20:00',
    homeTeam: 'ALG',
    awayTeam: 'SUD',
    stadium: 'Stade Prince Moulay Abdellah',
    city: 'Rabat',
    group: 'E',
    stage: 'group',
  },

  // ... (Plus de matchs à ajouter pour phases finales)
];

// Dates clés du tournoi
export const TOURNAMENT_INFO = {
  name: 'CAN 2025',
  fullName: 'Coupe d\'Afrique des Nations 2025',
  host: 'Maroc 🇲🇦',
  startDate: '2025-12-21',
  endDate: '2026-01-18',
  teamsCount: 24,
  groupsCount: 6,
  stadiums: [
    'Stade Mohammed V (Casablanca)',
    'Stade Prince Moulay Abdellah (Rabat)',
    'Stade Grand Stade de Marrakech',
    'Stade Adrar (Agadir)',
    'Stade de Fès',
    'Stade de Tanger',
  ],
};

// Effectif Algérie (simplifié - à compléter)
export const ALGERIA_SQUAD = {
  coach: 'Vladimir Petković',
  captains: ['Riyad Mahrez', 'Aïssa Mandi'],
  keyPlayers: [
    { name: 'Riyad Mahrez', position: 'Attaquant', club: 'Al-Ahli' },
    { name: 'Islam Slimani', position: 'Attaquant', club: 'Al-Ittihad' },
    { name: 'Youcef Belaïli', position: 'Ailier', club: 'MC Alger' },
    { name: 'Ismaël Bennacer', position: 'Milieu', club: 'AC Milan' },
    { name: 'Aïssa Mandi', position: 'Défenseur', club: 'Lille' },
    { name: 'Ramy Bensebaïni', position: 'Défenseur', club: 'Dortmund' },
    { name: 'Alexandre Oukidja', position: 'Gardien', club: 'Metz' },
  ],
  titles: {
    canWins: 2, // 1990, 2019
    lastTitle: 2019,
    bestResult: 'Champions',
  },
};

// Helper functions
export function getTeamById(id: string): Team | undefined {
  return TEAMS.find(team => team.id === id);
}

export function getMatchesByTeam(teamId: string): Match[] {
  return ALL_MATCHES.filter(
    match => match.homeTeam === teamId || match.awayTeam === teamId
  );
}

export function getGroupMatches(groupName: string): Match[] {
  return ALL_MATCHES.filter(match => match.group === groupName);
}

export function getMatchesByDate(date: string): Match[] {
  return ALL_MATCHES.filter(match => match.date === date);
}

// Calculate days until tournament start
export function getDaysUntilStart(): number {
  const now = new Date();
  const start = new Date(TOURNAMENT_INFO.startDate);
  const diff = start.getTime() - now.getTime();
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24));
  return days > 0 ? days : 0;
}

// Calculate days until Algeria's first match
export function getDaysUntilAlgeriaMatch(): number {
  const now = new Date();
  const firstMatch = new Date(ALGERIA_MATCHES[0].date);
  const diff = firstMatch.getTime() - now.getTime();
  const days = Math.ceil(diff / (1000 * 60 * 60 * 24));
  return days > 0 ? days : 0;
}
