<?php
/**
 * BBC School Algeria - Intégration Chatbot
 * Connexion entre le chatbot BotBuddy et le système BBC School existant
 */

// Configuration BBC School
require_once '../config/bbc_stats.php';

// Connexion base de données
try {
    $pdo = new PDO("mysql:host=localhost;dbname=onest_school;charset=utf8", 'root', '');
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die("Erreur de connexion: " . $e->getMessage());
}

// Charger les statistiques BBC
$bbc_config = include '../config/bbc_stats.php';

// Récupérer les vraies statistiques
$stmt = $pdo->query("SELECT COUNT(*) as count FROM staff WHERE role_id = 2"); // Teachers
$teachers_count = $stmt->fetch()['count'];

$stmt = $pdo->query("SELECT COUNT(*) as count FROM staff WHERE role_id = 3"); // Students  
$students_count = $stmt->fetch()['count'];

$stmt = $pdo->query("SELECT COUNT(*) as count FROM staff WHERE role_id = 4"); // Parents
$parents_count = $stmt->fetch()['count'];

// API pour le chatbot
if (isset($_GET['api'])) {
    header('Content-Type: application/json; charset=utf-8');
    
    switch ($_GET['api']) {
        case 'stats':
            echo json_encode([
                'school_name' => $bbc_config['school_name'],
                'school_name_ar' => $bbc_config['school_name_ar'],
                'school_name_fr' => $bbc_config['school_name_fr'],
                'stats' => [
                    'students' => (int)$students_count,
                    'teachers' => (int)$teachers_count,
                    'parents' => (int)$parents_count,
                    'classes' => $bbc_config['current_stats']['classes']
                ],
                'last_updated' => $bbc_config['last_updated'],
                'facebook_page' => 'https://www.facebook.com/bbc.bestbridgeforcreation/',
                'chatbot_active' => true
            ]);
            break;
            
        case 'languages':
            $stmt = $pdo->query("SELECT * FROM languages ORDER BY id");
            $languages = $stmt->fetchAll(PDO::FETCH_ASSOC);
            echo json_encode(['languages' => $languages]);
            break;
            
        case 'chat_history':
            // Simuler l'historique des chats
            echo json_encode([
                'conversations' => [
                    ['id' => 1, 'user' => 'Parent', 'message' => 'Information about enrollment', 'time' => '10:30'],
                    ['id' => 2, 'user' => 'Student', 'message' => 'Class schedules', 'time' => '11:15'],
                    ['id' => 3, 'user' => 'Visitor', 'message' => 'School programs', 'time' => '14:20']
                ]
            ]);
            break;
            
        default:
            echo json_encode(['error' => 'API endpoint not found']);
    }
    exit;
}

// Interface d'administration
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BBC School Algeria - Chatbot Integration</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #1e3d59 0%, #2980b9 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        
        .integration-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 3rem;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
            max-width: 600px;
            width: 90%;
        }
        
        .bbc-logo {
            width: 80px;
            height: 80px;
            background: white;
            border-radius: 15px;
            margin: 0 auto 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #1e3d59;
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            font-weight: 700;
        }
        
        .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 2rem;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .stat-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #ff6b35;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        .action-buttons {
            display: flex;
            gap: 1rem;
            margin-top: 2rem;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .btn {
            padding: 1rem 2rem;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .btn-primary {
            background: #ff6b35;
            color: white;
        }
        
        .btn-secondary {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(46, 204, 113, 0.2);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            background: #2ecc71;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .facebook-link {
            margin-top: 1rem;
            padding: 1rem;
            background: rgba(24, 119, 242, 0.2);
            border-radius: 10px;
            border: 1px solid rgba(24, 119, 242, 0.3);
        }
        
        .facebook-link a {
            color: #1877f2;
            text-decoration: none;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="integration-container">
        <div class="bbc-logo">
            <span>BBC</span>
        </div>
        
        <h1>🤖 Chatbot Intégré</h1>
        <p class="subtitle">BBC School Algeria - AI Assistant</p>
        
        <div class="status-indicator">
            <div class="status-dot"></div>
            <span>Système Actif</span>
        </div>
        
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-number"><?php echo $students_count; ?></div>
                <div class="stat-label">Étudiants</div>
            </div>
            <div class="stat-item">
                <div class="stat-number"><?php echo $teachers_count; ?></div>
                <div class="stat-label">Professeurs</div>
            </div>
            <div class="stat-item">
                <div class="stat-number"><?php echo $parents_count; ?></div>
                <div class="stat-label">Parents</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">3</div>
                <div class="stat-label">Langues</div>
            </div>
        </div>
        
        <div class="action-buttons">
            <a href="chatbot-dashboard.html" class="btn btn-primary">
                <i class="fas fa-robot"></i>
                Ouvrir Dashboard Chatbot
            </a>
            <a href="../public/index.php" class="btn btn-secondary">
                <i class="fas fa-home"></i>
                Retour BBC School
            </a>
        </div>
        
        <div class="facebook-link">
            <i class="fab fa-facebook"></i>
            <a href="https://www.facebook.com/bbc.bestbridgeforcreation/" target="_blank">
                Suivez-nous sur Facebook
            </a>
        </div>
        
        <div style="margin-top: 2rem; font-size: 0.9rem; opacity: 0.7;">
            <p>🌍 Interface trilingue: العربية / Français / English</p>
            <p>✨ Propulsé par BotBuddy Template + BBC School Data</p>
        </div>
    </div>
    
    <script>
        console.log('🏫 BBC School Algeria Chatbot Integration Ready!');
        console.log('📊 Real-time stats loaded from database');
        console.log('🤖 BotBuddy template successfully integrated');
        console.log('🔗 Facebook: https://www.facebook.com/bbc.bestbridgeforcreation/');
    </script>
</body>
</html>