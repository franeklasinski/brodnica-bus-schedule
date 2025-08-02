class RoutePlannerApp {
    constructor() {
        this.allStops = [];
        this.currentRoutes = [];
        this.init();
    }

    init() {
        this.updateCurrentTime();
        this.loadAllStops();
        this.loadLegend();
        this.loadScheduleInfo();
        this.bindEvents();
        
        // Aktualizuj czas co 30 sekund
        setInterval(() => this.updateCurrentTime(), 30000);
        
        // Odświeżaj dane co 60 sekund
        setInterval(() => {
            this.showRefreshIndicator();
            this.loadScheduleInfo();
            if (this.currentRoutes.length > 0) {
                this.refreshCurrentRoutes();
            }
            setTimeout(() => this.hideRefreshIndicator(), 1000);
        }, 60000);
    }

    showRefreshIndicator() {
        const indicator = document.getElementById('refreshIndicator');
        if (indicator) {
            indicator.classList.add('refreshing');
        }
    }

    hideRefreshIndicator() {
        const indicator = document.getElementById('refreshIndicator');
        if (indicator) {
            indicator.classList.remove('refreshing');
        }
    }

    updateCurrentTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('pl-PL', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        const dateString = now.toLocaleDateString('pl-PL', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        const timeElement = document.getElementById('currentTime');
        if (timeElement) {
            timeElement.innerHTML = `
                <i class="fas fa-clock"></i> 
                ${timeString} • ${dateString}
            `;
        }
    }

    async loadAllStops() {
        try {
            this.showLoading(true);
            const response = await fetch('/api/all-stops');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            this.allStops = await response.json();
            this.populateStopSelects();
        } catch (error) {
            console.error('Błąd podczas ładowania przystanków:', error);
            this.showError('Nie udało się załadować przystanków. Spróbuj ponownie.');
        } finally {
            this.showLoading(false);
        }
    }

    populateStopSelects() {
        const fromSelect = document.getElementById('fromStop');
        const toSelect = document.getElementById('toStop');
        
        if (!fromSelect || !toSelect) return;
        
        // Wyczyść opcje (pozostaw pierwszą - placeholder)
        fromSelect.innerHTML = '<option value="">Wybierz przystanek startowy...</option>';
        toSelect.innerHTML = '<option value="">Wybierz przystanek docelowy...</option>';
        
        // Dodaj wszystkie przystanki
        this.allStops.forEach(stop => {
            const linesInfo = stop.lines.map(line => `L${line.number}`).join(', ');
            const optionText = `${stop.name} (${linesInfo})`;
            
            const fromOption = new Option(optionText, stop.id);
            const toOption = new Option(optionText, stop.id);
            
            fromSelect.appendChild(fromOption);
            toSelect.appendChild(toOption);
        });
    }

    async findRoutes() {
        const fromStop = document.getElementById('fromStop').value;
        const toStop = document.getElementById('toStop').value;
        
        if (!fromStop || !toStop) {
            this.showError('Wybierz oba przystanki');
            return;
        }
        
        if (fromStop === toStop) {
            this.showError('Przystanek startowy i docelowy nie mogą być takie same');
            return;
        }
        
        try {
            this.showLoading(true);
            const response = await fetch(`/api/routes/${fromStop}/${toStop}`);
            
            if (!response.ok) {
                if (response.status === 404) {
                    const errorData = await response.json();
                    this.showError(errorData.message || 'Brak bezpośrednich połączeń');
                    return;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.currentRoutes = data.routes;
            this.showRouteResults(data);
        } catch (error) {
            console.error('Błąd podczas wyszukiwania tras:', error);
            this.showError('Nie udało się znaleźć połączeń. Spróbuj ponownie.');
        } finally {
            this.showLoading(false);
        }
    }

    showRouteResults(data) {
        const routePlanner = document.getElementById('routePlanner');
        const routeResults = document.getElementById('routeResults');
        const routeTitle = document.getElementById('routeTitle');
        const routesContainer = document.getElementById('routesContainer');
        
        if (routePlanner) routePlanner.style.display = 'none';
        if (routeResults) routeResults.style.display = 'block';
        
        if (routeTitle) {
            routeTitle.innerHTML = `
                <i class="fas fa-route"></i> 
                ${data.from_stop_name} → ${data.to_stop_name}
                <span class="route-count">(${data.total_options} ${data.total_options === 1 ? 'opcja' : 'opcje'})</span>
            `;
        }
        
        if (routesContainer) {
            routesContainer.innerHTML = this.renderRoutes(data.routes);
        }
    }

    renderRoutes(routes) {
        return routes.map(route => {
            const nextDeparture = route.from_stop.next_departures[0];
            const departuresHtml = route.from_stop.departures.map((time, index) => {
                const nextTimes = route.from_stop.next_departures.map(d => d.time);
                let cssClass = 'departure-time';
                let timeUntil = '';
                
                if (nextTimes.includes(time)) {
                    const departure = route.from_stop.next_departures.find(d => d.time === time);
                    if (departure) {
                        if (departure.minutes_until <= 5) {
                            cssClass += ' next';
                        } else if (departure.minutes_until <= 15) {
                            cssClass += ' soon';
                        }
                        timeUntil = `<div class="time-until">${this.formatTimeUntil(departure.minutes_until)}</div>`;
                    }
                }
                
                return `
                    <div class="${cssClass}">
                        ${time}
                        ${timeUntil}
                    </div>
                `;
            }).join('');

            return `
                <div class="route-card fade-in" style="--line-color: ${route.line_color}">
                    <div class="route-header">
                        <div class="bus-number" style="background-color: ${route.line_color}">${route.line_number}</div>
                        <div class="route-info">
                            <div class="route-name">${route.line_name}</div>
                            <div class="travel-info">
                                <i class="fas fa-clock"></i> 
                                Czas podróży: ~${route.estimated_travel_time} min
                                ${route.stops_between > 0 ? `• ${route.stops_between} przyst.` : '• bezpośrednio'}
                            </div>
                        </div>
                        <button class="expand-route-btn" onclick="app.toggleRouteDetails('${route.line_number}', '${route.from_stop.id}', '${route.to_stop.id}', this)">
                            <i class="fas fa-chevron-down"></i>
                        </button>
                    </div>
                    
                    <div class="departure-info">
                        <div class="next-departure">
                            <i class="fas fa-play"></i> 
                            Najbliższy odjazd: <strong>${nextDeparture ? nextDeparture.time : 'Brak'}</strong>
                            ${nextDeparture ? `<span class="time-until-badge">${this.formatTimeUntil(nextDeparture.minutes_until)}</span>` : ''}
                        </div>
                        
                        <div class="all-departures">
                            <h4>Wszystkie odjazdy z ${route.from_stop.name}:</h4>
                            <div class="departures-grid">
                                ${departuresHtml}
                            </div>
                        </div>
                    </div>
                    
                    <div class="route-details" id="route-details-${route.line_number}-${route.from_stop.id}-${route.to_stop.id}" style="display: none;">
                        <div class="route-details-loading">
                            <i class="fas fa-spinner fa-spin"></i> Ładowanie szczegółów trasy...
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    formatTimeUntil(minutes) {
        if (minutes < 0) minutes += 24 * 60; // Następny dzień
        
        if (minutes === 0) return 'Teraz';
        if (minutes === 1) return '1 min';
        if (minutes < 60) return `${minutes} min`;
        
        const hours = Math.floor(minutes / 60);
        const remainingMinutes = minutes % 60;
        
        if (hours === 1 && remainingMinutes === 0) return '1 godz';
        if (hours === 1) return `1 godz ${remainingMinutes} min`;
        if (remainingMinutes === 0) return `${hours} godz`;
        
        return `${hours} godz ${remainingMinutes} min`;
    }

    swapStops() {
        const fromSelect = document.getElementById('fromStop');
        const toSelect = document.getElementById('toStop');
        
        if (fromSelect && toSelect) {
            const temp = fromSelect.value;
            fromSelect.value = toSelect.value;
            toSelect.value = temp;
            
            this.updateFindButton();
        }
    }

    updateFindButton() {
        const fromStop = document.getElementById('fromStop').value;
        const toStop = document.getElementById('toStop').value;
        const findButton = document.getElementById('findRoutes');
        
        if (findButton) {
            findButton.disabled = !fromStop || !toStop || fromStop === toStop;
        }
    }

    backToPlanner() {
        const routePlanner = document.getElementById('routePlanner');
        const routeResults = document.getElementById('routeResults');
        
        if (routePlanner) routePlanner.style.display = 'block';
        if (routeResults) routeResults.style.display = 'none';
        
        this.currentRoutes = [];
    }

    async toggleRouteDetails(lineNumber, fromStopId, toStopId, button) {
        const detailsId = `route-details-${lineNumber}-${fromStopId}-${toStopId}`;
        const detailsElement = document.getElementById(detailsId);
        const icon = button.querySelector('i');
        
        if (!detailsElement) return;
        
        if (detailsElement.style.display === 'none') {
            detailsElement.style.display = 'block';
            icon.className = 'fas fa-chevron-up';
            button.classList.add('expanded');
            
            if (detailsElement.innerHTML.includes('Ładowanie')) {
                await this.loadRouteDetails(lineNumber, fromStopId, toStopId, detailsElement);
            }
        } else {
            detailsElement.style.display = 'none';
            icon.className = 'fas fa-chevron-down';
            button.classList.remove('expanded');
        }
    }

    async loadRouteDetails(lineNumber, fromStopId, toStopId, detailsElement) {
        try {
            const response = await fetch(`/api/route-details/${lineNumber}/${fromStopId}/${toStopId}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const details = await response.json();
            this.renderRouteDetails(details, detailsElement);
        } catch (error) {
            console.error('Błąd podczas ładowania szczegółów trasy:', error);
            detailsElement.innerHTML = `
                <div class="route-details-error">
                    <i class="fas fa-exclamation-triangle"></i>
                    Nie udało się załadować szczegółów trasy
                </div>
            `;
        }
    }

    renderRouteDetails(details, detailsElement) {
        const routeStopsHtml = details.route_stops.map(stop => {
            let stopClass = 'route-stop';
            let stopIcon = 'fas fa-circle';
            
            if (stop.is_origin) {
                stopClass += ' origin';
                stopIcon = 'fas fa-play-circle';
            } else if (stop.is_destination) {
                stopClass += ' destination';
                stopIcon = 'fas fa-flag-checkered';
            } else {
                stopClass += ' intermediate';
            }
            
            return `
                <div class="${stopClass}">
                    <div class="stop-icon">
                        <i class="${stopIcon}"></i>
                    </div>
                    <div class="stop-info">
                        <div class="stop-name">${stop.name}</div>
                        <div class="stop-time">
                            ${stop.arrival_time}
                            ${stop.minutes_from_start > 0 ? `(+${stop.minutes_from_start} min)` : '(start)'}
                        </div>
                    </div>
                </div>
            `;
        }).join('');
        
        detailsElement.innerHTML = `
            <div class="route-details-header">
                <h4>
                    <i class="fas fa-route"></i>
                    Szczegółowa trasa - Linia ${details.line_number}
                </h4>
                <div class="route-summary">
                    <span><i class="fas fa-clock"></i> Odjazd: ${details.departure_time}</span>
                    <span><i class="fas fa-stopwatch"></i> Całkowity czas: ${details.total_travel_time} min</span>
                    <span><i class="fas fa-map-marker-alt"></i> Przystanków: ${details.total_stops}</span>
                </div>
            </div>
            <div class="route-timeline">
                ${routeStopsHtml}
            </div>
        `;
    }

    async loadLegend() {
        try {
            const response = await fetch('/api/legend');
            if (!response.ok) return;
            
            const legend = await response.json();
            this.renderLegend(legend);
        } catch (error) {
            console.error('Błąd podczas ładowania legendy:', error);
        }
    }

    renderLegend(legend) {
        const legendContent = document.getElementById('legendContent');
        if (!legendContent) return;

        let legendHTML = `
            <div class="legend-date">
                <i class="fas fa-calendar-alt"></i> ${legend.date}
            </div>
            <div class="legend-content">
        `;

        if (legend.line_info) {
            legendHTML += `
                <div class="legend-item">
                    <strong><i class="fas fa-bus"></i> Linie autobusowe:</strong>
                    ${Object.entries(legend.line_info).map(([line, info]) => 
                        `<div class="line-item">Linia ${line}: ${info.replace(`Linia ${line}: `, '')}</div>`
                    ).join('')}
                </div>
            `;
        }

        if (legend.features) {
            legendHTML += `
                <div class="legend-item">
                    <strong><i class="fas fa-star"></i> Funkcje systemu:</strong>
                    ${Object.entries(legend.features).map(([feature, description]) => 
                        `<div class="feature-item"><strong>${feature}:</strong> ${description}</div>`
                    ).join('')}
                </div>
            `;
        }

        if (legend.technical_info) {
            legendHTML += `
                <div class="legend-item">
                    <strong><i class="fas fa-cog"></i> Informacje techniczne:</strong>
                    ${Object.entries(legend.technical_info).map(([tech, info]) => 
                        `<div class="tech-item"><strong>${tech}:</strong> ${info}</div>`
                    ).join('')}
                </div>
            `;
        }

        legendHTML += `
                <div class="legend-item">
                    <strong><i class="fas fa-info-circle"></i> Dodatkowe informacje:</strong>
                    <div class="note-item">${legend.note}</div>
                    <div class="note-item">System pokazuje wszystkie autobusy między wybranymi przystankami</div>
                </div>
            </div>
        `;

        legendContent.innerHTML = legendHTML;
    }

    async loadScheduleInfo() {
        try {
            const response = await fetch('/api/legend');
            if (!response.ok) return;
            
            const legend = await response.json();
            this.updateScheduleInfo(legend);
        } catch (error) {
            console.error('Błąd podczas ładowania informacji o rozkładzie:', error);
            const dayTypeElement = document.getElementById('dayTypeInfo');
            if (dayTypeElement) {
                dayTypeElement.textContent = 'Nie udało się pobrać informacji o rozkładzie';
            }
        }
    }

    async refreshCurrentRoutes() {
        const fromSelect = document.getElementById('fromStop');
        const toSelect = document.getElementById('toStop');
        
        if (fromSelect && toSelect && fromSelect.value && toSelect.value) {
            // Cicho odśwież trasy w tle
            try {
                const response = await fetch(`/api/routes/${fromSelect.value}/${toSelect.value}`);
                if (response.ok) {
                    const data = await response.json();
                    this.currentRoutes = data.routes || [];
                    this.renderRoutes(data);
                }
            } catch (error) {
                console.log('Błąd podczas odświeżania tras:', error);
            }
        }
    }

    updateScheduleInfo(legend) {
        const dayTypeElement = document.getElementById('dayTypeInfo');
        if (dayTypeElement) {
            dayTypeElement.innerHTML = `
                <strong>Rozkład jazdy:</strong> Brodnica - autobusy miejskie
            `;
        }
    }

    bindEvents() {
        const findButton = document.getElementById('findRoutes');
        const swapButton = document.getElementById('swapStops');
        const backButton = document.getElementById('backToPlanner');
        const fromSelect = document.getElementById('fromStop');
        const toSelect = document.getElementById('toStop');
        
        if (findButton) {
            findButton.addEventListener('click', () => this.findRoutes());
        }
        
        if (swapButton) {
            swapButton.addEventListener('click', () => this.swapStops());
        }
        
        if (backButton) {
            backButton.addEventListener('click', () => this.backToPlanner());
        }
        
        if (fromSelect) {
            fromSelect.addEventListener('change', () => this.updateFindButton());
        }
        
        if (toSelect) {
            toSelect.addEventListener('change', () => this.updateFindButton());
        }
        
        setInterval(() => {
            if (this.currentRoutes.length > 0) {
                const fromStop = document.getElementById('fromStop').value;
                const toStop = document.getElementById('toStop').value;
                if (fromStop && toStop) {
                    this.findRoutes();
                }
            }
        }, 30000);
    }

    showLoading(show) {
        const loading = document.getElementById('loading');
        if (loading) {
            loading.style.display = show ? 'flex' : 'none';
        }
    }

    showError(message) {
        alert(message);
    }
}

// AI Chatbot
class AIChatbot {
    constructor() {
        this.isExpanded = false;
        this.isLoading = false;
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupInitialState();
    }

    setupInitialState() {
        const content = document.getElementById('chatbotContent');
        const toggle = document.getElementById('chatbotToggle');
        
        if (content && toggle) {
            content.classList.add('collapsed');
            toggle.classList.remove('expanded');
        }
    }

    bindEvents() {
        const header = document.querySelector('.chatbot-header');
        const sendButton = document.getElementById('sendMessage');
        const chatInput = document.getElementById('chatInput');

        if (header) {
            header.addEventListener('click', () => this.toggleChatbot());
        }

        if (sendButton) {
            sendButton.addEventListener('click', () => this.sendMessage());
        }

        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !this.isLoading) {
                    this.sendMessage();
                }
            });

            chatInput.addEventListener('input', () => {
                this.updateSendButtonState();
            });
        }
    }

    toggleChatbot() {
        const content = document.getElementById('chatbotContent');
        const toggle = document.getElementById('chatbotToggle');

        if (content && toggle) {
            this.isExpanded = !this.isExpanded;
            
            if (this.isExpanded) {
                content.classList.remove('collapsed');
                toggle.classList.add('expanded');
            } else {
                content.classList.add('collapsed');
                toggle.classList.remove('expanded');
            }
        }
    }

    updateSendButtonState() {
        const input = document.getElementById('chatInput');
        const button = document.getElementById('sendMessage');
        
        if (input && button) {
            const hasText = input.value.trim().length > 0;
            button.disabled = !hasText || this.isLoading;
        }
    }

    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input?.value.trim();

        if (!message || this.isLoading) return;

        // Pokaż wiadomość użytkownika
        this.addMessage(message, 'user');
        
        // Wyczyść input
        input.value = '';
        this.updateSendButtonState();

        // Pokaż loading
        this.showLoading();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message: message,
                    context: {
                        current_page: 'route_planner',
                        timestamp: new Date().toISOString()
                    }
                })
            });

            const data = await response.json();
            
            this.hideLoading();

            if (response.ok && data.response) {
                this.addMessage(data.response, 'bot');
            } else {
                this.addMessage(
                    data.response || '🚌 Przepraszam, nie mogę teraz odpowiedzieć. Spróbuj zadać pytanie inaczej lub sprawdź rozkład ręcznie.', 
                    'bot'
                );
            }

        } catch (error) {
            console.error('Błąd chatbota:', error);
            this.hideLoading();
            this.addMessage(
                '🚌 Wystąpił problem z połączeniem. Sprawdź internet i spróbuj ponownie za chwilę.', 
                'bot'
            );
        }
    }

    addMessage(content, type) {
        const messagesContainer = document.getElementById('chatMessages');
        if (!messagesContainer) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type}-message`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        if (type === 'user') {
            contentDiv.innerHTML = `<i class="fas fa-user"></i>${content}`;
        } else {
            contentDiv.innerHTML = `<i class="fas fa-robot"></i>${content}`;
        }

        messageDiv.appendChild(contentDiv);
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    showLoading() {
        this.isLoading = true;
        this.updateSendButtonState();
        
        const loadingMessage = document.createElement('div');
        loadingMessage.className = 'chat-message bot-message';
        loadingMessage.id = 'loading-message';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content chat-loading';
        contentDiv.innerHTML = '<i class="fas fa-robot"></i>Myślę';
        
        loadingMessage.appendChild(contentDiv);
        
        const messagesContainer = document.getElementById('chatMessages');
        if (messagesContainer) {
            messagesContainer.appendChild(loadingMessage);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }

    hideLoading() {
        this.isLoading = false;
        this.updateSendButtonState();
        
        const loadingMessage = document.getElementById('loading-message');
        if (loadingMessage) {
            loadingMessage.remove();
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.app = new RoutePlannerApp();
    window.chatbot = new AIChatbot();
});
