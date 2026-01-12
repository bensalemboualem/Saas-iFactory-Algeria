#\!/bin/bash
cd /opt/iafactory-rag-dz/interview-agents
pkill -f "next.*3738"
sleep 3
nohup npm run start > /var/log/interview-agents.log 2>&1 &
echo "Application démarrée"
sleep 25
netstat -tlnp | grep 3738
ps aux | grep "next.*3738" | grep -v grep
tail -15 /var/log/interview-agents.log
curl -s -o /dev/null -w "Test /interview: %{http_code}\n" http://localhost:3738/interview
