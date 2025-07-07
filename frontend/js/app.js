document.addEventListener('DOMContentLoaded', function() {
    const matchesContainer = document.getElementById('matches-container');
    const lastUpdatedSpan = document.getElementById('last-updated');

    // 核心修改：将fetch的地址从本地文件改为后端的API接口
    fetch('/api/matches') // 不再是 '../data/matches.json'
        .then(response => {
            if (!response.ok) {
                // 如果服务器返回错误状态码 (如500), 也在这里处理
                throw new Error(`服务器错误! 状态码: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // 检查后端是否返回了我们定义的错误信息
            if (data.error) {
                throw new Error(data.error);
            }
            
            matchesContainer.innerHTML = ''; // 清除加载动画
            
            if (data && data.length > 0) {
                data.forEach(match => {
                    const matchCard = createMatchCard(match);
                    matchesContainer.appendChild(matchCard);
                });
            } else {
                matchesContainer.innerHTML = '<p>当前没有可显示的比赛数据。</p>';
            }

            // 更新时间戳
            lastUpdatedSpan.textContent = new Date().toLocaleString('zh-CN');
        })
        .catch(error => {
            console.error('加载比赛数据时出错:', error);
            // 显示更具体的错误信息给用户
            matchesContainer.innerHTML = `<p style="color: red;">无法加载比赛数据: ${error.message}。请检查后端服务器是否已启动并能正常工作。</p>`;
        });

    // createMatchCard 函数保持不变
    function createMatchCard(match) {
        // ... (这里的代码和之前完全一样，无需改动)
        const card = document.createElement('div');
        card.className = 'match-card';
        const goalLine = parseFloat(match.hhad.goalLine);
        const goalLineText = goalLine > 0 ? `+${goalLine}` : goalLine;
        card.innerHTML = `
            <div class="match-header">
                <span class="league-name">${match.leagueName}</span>
                <span class="match-num">${match.matchNum}</span>
            </div>
            <div class="teams">
                <span class="team-name">${match.homeTeamName}</span>
                <span class="vs">VS</span>
                <span class="team-name">${match.awayTeamName}</span>
            </div>
            <p style="text-align:center; font-size:0.9em; color:#666;">比赛时间: ${match.matchTime}</p>
            <div class="odds-section">
                <table class="odds-table">
                    <thead>
                        <tr>
                            <th>玩法</th>
                            <th>主胜</th>
                            <th>平</th>
                            <th>客胜</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="odds-type">胜平负</td>
                            <td class="odds-value win">${match.had.h}</td>
                            <td class="odds-value draw">${match.had.d}</td>
                            <td class="odds-value lose">${match.had.a}</td>
                        </tr>
                        <tr>
                            <td class="odds-type">让球 (${goalLineText})</td>
                            <td class="odds-value win">${match.hhad.h}</td>
                            <td class="odds-value draw">${match.hhad.d}</td>
                            <td class="odds-value lose">${match.hhad.a}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `;
        return card;
    }
});