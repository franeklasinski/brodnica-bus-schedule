from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import json
import ollama

app = Flask(__name__)

bus_lines = {
    "1": {
        "name": "Linia 1: Michałowo pętla ↔ Grunwald pętla",
        "color": "#e74c3c",
        "stops": {
            "michałowo_petla": {
                "name": "00 - Michałowo pętla",
                "departures": ["06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "10:00", "11:00", "12:00", "12:53", "13:43", "14:35", "15:30", "16:35", "19:20"],
                "position": 0
            },
            "lidzbarska": {
                "name": "01 - Lidzbarska", 
                "departures": ["06:33", "07:03", "07:33", "08:03", "08:33", "09:03", "10:03", "11:03", "12:03", "12:56", "13:46", "14:38", "15:33", "16:38", "19:23"],
                "position": 1
            },
            "lidzbarska_2": {
                "name": "02 - Lidzbarska",
                "departures": ["06:35", "07:05", "07:35", "08:05", "08:35", "09:05", "10:05", "11:05", "12:05", "12:58", "13:48", "14:40", "15:35", "16:40", "19:25"],
                "position": 2
            },
            "matejki_1": {
                "name": "03 - Matejki I",
                "departures": ["06:38", "07:08", "07:38", "08:08", "08:38", "09:08", "10:08", "11:08", "12:08", "13:01", "13:51", "14:43", "15:38", "16:43", "19:28"],
                "position": 3
            },
            "wyspiańskiego_2": {
                "name": "04 - Wyspiańskiego II",
                "departures": ["06:40", "07:10", "07:40", "08:10", "08:40", "09:10", "10:10", "11:10", "12:10", "13:03", "13:53", "14:45", "15:40", "16:45", "19:30"],
                "position": 4
            },
            "wyspiańskiego": {
                "name": "05 - Wyspiańskiego",
                "departures": ["06:43", "07:13", "07:43", "08:13", "08:43", "09:13", "10:13", "11:13", "12:13", "13:06", "13:56", "14:48", "15:43", "16:48", "19:33"],
                "position": 5
            },
            "stycznia_18": {
                "name": "06 - 18 Stycznia",
                "departures": ["06:46", "07:16", "07:46", "08:16", "08:46", "09:16", "10:16", "11:16", "12:16", "13:09", "13:59", "14:51", "15:46", "16:51", "19:36"],
                "position": 6
            },
            "mazurska": {
                "name": "10 - Mazurska",
                "departures": ["06:50", "07:20", "07:50", "08:20", "08:50", "09:20", "10:20", "11:20", "12:20", "13:13", "14:03", "14:55", "15:50", "16:55", "19:40"],
                "position": 7
            },
            "przykop": {
                "name": "11 - Przykop",
                "departures": ["06:53", "07:23", "07:53", "08:23", "08:53", "09:23", "10:23", "11:23", "12:23", "13:16", "14:06", "14:58", "15:53", "16:58", "19:43"],
                "position": 8
            },
            "przykop_1": {
                "name": "12 - Przykop I",
                "departures": ["06:55", "07:25", "07:55", "08:25", "08:55", "09:25", "10:25", "11:25", "12:25", "13:18", "14:08", "15:00", "15:55", "17:00", "19:45"],
                "position": 9
            },
            "przykop_2": {
                "name": "13 - Przykop II", 
                "departures": ["06:58", "07:28", "07:58", "08:28", "08:58", "09:28", "10:28", "11:28", "12:28", "13:21", "14:11", "15:03", "15:58", "17:03", "19:48"],
                "position": 10
            },
            "kamionka": {
                "name": "14 - Kamionka",
                "departures": ["07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:30", "11:30", "12:30", "13:23", "14:13", "15:05", "16:00", "17:05", "19:50"],
                "position": 11
            },
            "sądowa": {
                "name": "17 - Sądowa",
                "departures": ["07:03", "07:33", "08:03", "08:33", "09:03", "09:33", "10:33", "11:33", "12:33", "13:26", "14:16", "15:08", "16:03", "17:08", "19:53"],
                "position": 12
            },
            "czarneckiego": {
                "name": "18 - Czarneckiego",
                "departures": ["07:05", "07:35", "08:05", "08:35", "09:05", "09:35", "10:35", "11:35", "12:35", "13:28", "14:18", "15:10", "16:05", "17:10", "19:55"],
                "position": 13
            },
            "wincentego_pola": {
                "name": "19 - Wincentego Pola",
                "departures": ["07:08", "07:38", "08:08", "08:38", "09:08", "09:38", "10:38", "11:38", "12:38", "13:31", "14:21", "15:13", "16:08", "17:13", "19:58"],
                "position": 14
            },
            "grunwald_petla": {
                "name": "20 - Grunwald pętla",
                "departures": ["07:13", "07:43", "08:13", "08:43", "09:13", "09:43", "10:43", "11:43", "12:43", "13:36", "14:26", "15:18", "16:13", "17:18", "20:03"],
                "position": 15
            }
        }
    },
    "2": {
        "name": "Linia 2: Saminex pętla ↔ Wapna pętla",
        "color": "#3498db",
        "stops": {
            "saminex_petla_2": {
                "name": "00 - Saminex pętla",
                "departures": ["06:00", "07:00", "08:00", "12:00", "14:00", "16:00", "18:00"]
            },
            "sikorskiego_cymir_2": {
                "name": "02 - Sikorskiego Cymir",
                "departures": ["06:03", "07:03", "08:03", "12:03", "14:03", "16:03", "18:03"]
            },
            "okrężna_cofresco_2": {
                "name": "04 - Okrężna Cofresco",
                "departures": ["06:06", "07:06", "08:06", "12:06", "14:06", "16:06", "18:06"]
            },
            "okrężna_2": {
                "name": "05 - Okrężna",
                "departures": ["06:08", "07:08", "08:08", "12:08", "14:08", "16:08", "18:08"]
            },
            "kolejowa_szkola_2": {
                "name": "07 - Kolejowa szkoła",
                "departures": ["06:11", "07:11", "08:11", "12:11", "14:11", "16:11", "18:11"]
            },
            "kolejowa_ii_2": {
                "name": "08 - Kolejowa II",
                "departures": ["06:12", "07:12", "08:12", "12:12", "14:12", "16:12", "18:12"]
            },
            "kolejowa_i_2": {
                "name": "09 - Kolejowa I",
                "departures": ["06:13", "07:13", "08:13", "12:13", "14:13", "16:13", "18:13"]
            },
            "zamkowa_2": {
                "name": "12 - Zamkowa",
                "departures": ["06:16", "07:16", "08:16", "12:16", "14:16", "16:16", "18:16"]
            },
            "sw_jakuba_2": {
                "name": "13 - Św. Jakuba",
                "departures": ["06:17", "07:17", "08:17", "12:17", "14:17", "16:17", "18:17"]
            },
            "koscielna_2": {
                "name": "14 - Kościelna",
                "departures": ["06:18", "07:18", "08:18", "12:18", "14:18", "16:18", "18:18"]
            },
            "maja_3_2": {
                "name": "16 - 3 Maja",
                "departures": ["06:20", "07:20", "08:20", "12:20", "14:20", "16:20", "18:20"]
            },
            "stycznia_18_2": {
                "name": "18 - 18 Stycznia",
                "departures": ["06:22", "07:22", "08:22", "12:22", "14:22", "16:22", "18:22"]
            },
            "ceglana_2": {
                "name": "19 - Ceglana",
                "departures": ["06:23", "07:23", "08:23", "12:23", "14:23", "16:23", "18:23"]
            },
            "wyspiańskiego_ii_2": {
                "name": "20 - Wyspiańskiego II",
                "departures": ["06:24", "07:24", "08:24", "12:24", "14:24", "16:24", "18:24"]
            },
            "wyspiańskiego_2": {
                "name": "21 - Wyspiańskiego",
                "departures": ["06:25", "07:25", "08:25", "12:25", "14:25", "16:25", "18:25"]
            },
            "nowa_2": {
                "name": "23 - Nowa",
                "departures": ["06:27", "07:27", "08:27", "12:27", "14:27", "16:27", "18:27"]
            },
            "nowa_i_2": {
                "name": "24 - Nowa I",
                "departures": ["06:28", "07:28", "08:28", "12:28", "14:28", "16:28", "18:28"]
            },
            "podgorna_vobro_2": {
                "name": "26 - Podgórna VOBRO",
                "departures": ["06:30", "07:30", "08:30", "12:30", "14:30", "16:30", "18:30"]
            },
            "dluga_ii_2": {
                "name": "27 - Długa II",
                "departures": ["06:31", "07:31", "08:31", "12:31", "14:31", "16:31", "18:31"]
            },
            "dluga_i_2": {
                "name": "28 - Długa I",
                "departures": ["06:32", "07:32", "08:32", "12:32", "14:32", "16:32", "18:32"]
            },
            "wapna_petla_2": {
                "name": "29 - Wapna pętla",
                "departures": ["06:35", "07:35", "08:35", "12:35", "14:35", "16:35", "18:35"]
            }
        }
    },
    "3": {
        "name": "Linia 3: Wyspiańskiego ↔ Łyskowskiego pętla",
        "color": "#2ecc71", 
        "stops": {
            "wyspiańskiego_3": {
                "name": "1 - Wyspiańskiego",
                "departures": ["11:20", "13:20", "15:20", "17:20"]
            },
            "wyspiańskiego_i_3": {
                "name": "2 - Wyspiańskiego I", 
                "departures": ["11:21", "13:21", "15:21", "17:21"]
            },
            "wyspiańskiego_ii_3": {
                "name": "3 - Wyspiańskiego II",
                "departures": ["11:22", "13:22", "15:22", "17:22"]
            },
            "ceglana_3": {
                "name": "4 - Ceglana",
                "departures": ["11:23", "13:23", "15:23", "17:23"]
            },
            "stycznia_18_3": {
                "name": "5 - 18 Stycznia",
                "departures": ["11:24", "13:24", "15:24", "17:24"]
            },
            "mazurska_3": {
                "name": "6 - Mazurska",
                "departures": ["11:28", "13:28", "15:28", "17:28"]
            },
            "przykop_3": {
                "name": "7 - Przykop",
                "departures": ["11:29", "13:29", "15:29", "17:29"]
            },
            "przykop_i_3": {
                "name": "8 - Przykop I",
                "departures": ["11:30", "13:30", "15:30", "17:30"]
            },
            "przykop_ii_3": {
                "name": "9 - Przykop II",
                "departures": ["11:31", "13:31", "15:31", "17:31"]
            },
            "kamionka_3": {
                "name": "10 - Kamionka",
                "departures": ["11:32", "13:32", "15:32", "17:32"]
            },
            "wiejska_3": {
                "name": "11 - Wiejska",
                "departures": ["11:34", "13:34", "15:34", "17:34"]
            },
            "niskie_brodno_3": {
                "name": "12 - Niskie Brodno",
                "departures": ["11:36", "13:36", "15:36", "17:36"]
            },
            "karbowska_3": {
                "name": "13 - Karbowska",
                "departures": ["11:38", "13:38", "15:38", "17:38"]
            },
            "powstancow_wielkopolskich_ii_3": {
                "name": "14 - Powstańców Wielkopolskich II",
                "departures": ["11:39", "13:39", "15:39", "17:39"]
            },
            "okrezna_szkola_3": {
                "name": "15 - Okrężna szkoła",
                "departures": ["11:40", "13:40", "15:40", "17:40"]
            },
            "lyskowskiego_3": {
                "name": "16 - Łyskowskiego",
                "departures": ["11:41", "13:41", "15:41", "17:41"]
            },
            "lyskowskiego_petla_3": {
                "name": "17 - Łyskowskiego pętla",
                "departures": ["11:42", "13:42", "15:42", "17:42"]
            }
        }
    },
    "4": {
        "name": "Linia 4: Saminex pętla ↔ Wyspiańskiego",
        "color": "#f39c12",
        "stops": {
            "saminex_petla_4": {
                "name": "00 - Saminex pętla",
                "departures": ["07:00", "09:00", "11:00", "13:00", "15:00", "17:00"]
            },
            "sikorskiego_cymir_4": {
                "name": "02 - Sikorskiego Cymir",
                "departures": ["07:02", "09:02", "11:02", "13:02", "15:02", "17:02"]
            },
            "sikorskiego_us_4": {
                "name": "03 - Sikorskiego US",
                "departures": ["07:03", "09:03", "11:03", "13:03", "15:03", "17:03"]
            },
            "sikorskiego_4": {
                "name": "04 - Sikorskiego", 
                "departures": ["07:04", "09:04", "11:04", "13:04", "15:04", "17:04"]
            },
            "kolejowa_i_4": {
                "name": "05 - Kolejowa I",
                "departures": ["07:05", "09:05", "11:05", "13:05", "15:05", "17:05"]
            },
            "dworzec_pkp_4": {
                "name": "07 - Dworzec PKP",
                "departures": ["07:07", "09:07", "11:07", "13:07", "15:07", "17:07"]
            },
            "zamkowa_4": {
                "name": "09 - Zamkowa",
                "departures": ["07:09", "09:09", "11:09", "13:09", "15:09", "17:09"]
            },
            "sw_jakuba_4": {
                "name": "10 - Św. Jakuba",
                "departures": ["07:10", "09:10", "11:10", "13:10", "15:10", "17:10"]
            },
            "koscielna_4": {
                "name": "11 - Kościelna",
                "departures": ["07:11", "09:11", "11:11", "13:11", "15:11", "17:11"]
            },
            "maja_3_4": {
                "name": "13 - 3 Maja",
                "departures": ["07:13", "09:13", "11:13", "13:13", "15:13", "17:13"]
            },
            "podgorna_zelatyna_4": {
                "name": "15 - Podgórna Żelatyna",
                "departures": ["07:15", "09:15", "11:15", "13:15", "15:15", "17:15"]
            },
            "grazyny_4": {
                "name": "16 - Grażyny",
                "departures": ["07:16", "09:16", "11:16", "13:16", "15:16", "17:16"]
            },
            "nowa_i_4": {
                "name": "17 - Nowa I",
                "departures": ["07:17", "09:17", "11:17", "13:17", "15:17", "17:17"]
            },
            "nowa_4": {
                "name": "18 - Nowa",
                "departures": ["07:18", "09:18", "11:18", "13:18", "15:18", "17:18"]
            },
            "poprzeczna_4": {
                "name": "19 - Poprzeczna",
                "departures": ["07:19", "09:19", "11:19", "13:19", "15:19", "17:19"]
            },
            "mieszka_i_4": {
                "name": "20 - Mieszka I",
                "departures": ["07:20", "09:20", "11:20", "13:20", "15:20", "17:20"]
            },
            "wyspiańskiego_4": {
                "name": "21 - Wyspiańskiego",
                "departures": ["07:21", "09:21", "11:21", "13:21", "15:21", "17:21"]
            }
        }
    },
    "5": {
        "name": "Linia 5: Saminex pętla ↔ Matejki",
        "color": "#9b59b6",
        "stops": {
            "saminex_petla_5": {
                "name": "00 - Saminex pętla",
                "departures": ["06:30", "08:30", "10:30", "14:30", "16:30", "18:30"]
            },
            "sikorskiego_cymir_5": {
                "name": "02 - Sikorskiego Cymir",
                "departures": ["06:32", "08:32", "10:32", "14:32", "16:32", "18:32"]
            },
            "okrezna_cofresco_5": {
                "name": "04 - Okrężna Cofresco",
                "departures": ["06:34", "08:34", "10:34", "14:34", "16:34", "18:34"]
            },
            "okrezna_5": {
                "name": "05 - Okrężna",
                "departures": ["06:35", "08:35", "10:35", "14:35", "16:35", "18:35"]
            },
            "graniczna_5": {
                "name": "07 - Graniczna",
                "departures": ["06:37", "08:37", "10:37", "14:37", "16:37", "18:37"]
            },
            "powstancow_wielkopolskich_ii_5": {
                "name": "08 - Powstańców Wielkopolskich II",
                "departures": ["06:38", "08:38", "10:38", "14:38", "16:38", "18:38"]
            },
            "karbowska_5": {
                "name": "09 - Karbowska",
                "departures": ["06:39", "08:39", "10:39", "14:39", "16:39", "18:39"]
            },
            "niskie_brodno_5": {
                "name": "11 - Niskie Brodno",
                "departures": ["06:41", "08:41", "10:41", "14:41", "16:41", "18:41"]
            },
            "wiejska_5": {
                "name": "13 - Wiejska",
                "departures": ["06:43", "08:43", "10:43", "14:43", "16:43", "18:43"]
            },
            "zamkowa_5": {
                "name": "15 - Zamkowa",
                "departures": ["06:45", "08:45", "10:45", "14:45", "16:45", "18:45"]
            },
            "sw_jakuba_5": {
                "name": "16 - Św. Jakuba",
                "departures": ["06:46", "08:46", "10:46", "14:46", "16:46", "18:46"]
            },
            "koscielna_5": {
                "name": "17 - Kościelna",
                "departures": ["06:47", "08:47", "10:47", "14:47", "16:47", "18:47"]
            },
            "maja_3_5": {
                "name": "19 - 3 Maja",
                "departures": ["06:49", "08:49", "10:49", "14:49", "16:49", "18:49"]
            },
            "lidzbarska_lo_5": {
                "name": "21 - Lidzbarska LO",
                "departures": ["06:51", "08:51", "10:51", "14:51", "16:51", "18:51"]
            },
            "matejki_5": {
                "name": "23 - Matejki",
                "departures": ["06:53", "08:53", "10:53", "14:53", "16:53", "18:53"]
            }
        }
    }
}

def get_day_type():
    """Określa typ dnia na podstawie aktualnej daty"""
    now = datetime.now()
    weekday = now.weekday()  #
    
    if weekday < 5:  
        return "workdays"
    elif weekday == 5: 
        return "saturdays"
    else:  
        return "sundays"

def parse_departure_time(time_str):
    """Parsuje czas odjazdu z oznaczeniami (T, S, L, *, /)"""

    clean_time = time_str.replace('T', '').replace('S', '').replace('L', '').replace('*', '').replace('/', '').replace('LD', '')
    
    if len(clean_time) == 4 and clean_time.isdigit():
        hours = clean_time[:2]
        minutes = clean_time[2:]
        return f"{hours}:{minutes}"
    
    if ':' in clean_time:
        return clean_time
    
    if len(clean_time) <= 2 and clean_time.isdigit():
        return clean_time
    
    return clean_time

def should_show_departure(time_str, day_type):
    """Sprawdza czy dany odjazd powinien być wyświetlony dla danego typu dnia"""

    if 'S' in time_str and day_type == 'sundays':
        return False  
    
    if 'L' in time_str and day_type != 'sundays':
        return False 
    
    return True

def get_departures_for_day(line_number, stop_id, day_type=None):
    """Pobiera odjazdy dla danego przystanku"""
    if line_number not in bus_lines:
        return []
    
    line = bus_lines[line_number]
    
    if 'stops' in line and stop_id in line['stops'] and 'departures' in line['stops'][stop_id]:
        return line['stops'][stop_id]['departures']
    
    return []

def get_next_departures(departures):
    """Sortuje odjazdy od najbliższego czasu"""
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    
    upcoming = []
    for dep_time in departures:
        dep_hour, dep_min = map(int, dep_time.split(':'))
        dep_datetime = now.replace(hour=dep_hour, minute=dep_min, second=0, microsecond=0)
        
        if dep_datetime < now:
            dep_datetime += timedelta(days=1)
            
        time_diff = (dep_datetime - now).total_seconds() / 60
        upcoming.append({
            'time': dep_time,
            'minutes_until': int(time_diff) if time_diff > 0 else int(time_diff + 24*60)
        })
    
    return sorted(upcoming, key=lambda x: x['minutes_until'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/lines')
def get_lines():
    """Zwraca listę wszystkich linii autobusowych"""
    lines = [{"number": k, "name": v["name"], "color": v["color"]} for k, v in bus_lines.items()]
    return jsonify(lines)

@app.route('/api/stops/<line_number>')
def get_stops_for_line(line_number):
    """Zwraca listę przystanków dla danej linii"""
    if line_number not in bus_lines:
        return jsonify({"error": "Linia nie znaleziona"}), 404
    
    line_info = bus_lines[line_number]
    stops = [{"id": k, "name": v["name"]} for k, v in line_info["stops"].items()]
    return jsonify({
        "line_name": line_info["name"],
        "line_color": line_info["color"],
        "stops": stops
    })

@app.route('/api/buses/<line_number>/<stop_id>')
def get_buses_for_stop(line_number, stop_id):
    """Zwraca busy dla danego przystanku na danej linii"""
    if line_number not in bus_lines:
        return jsonify({"error": "Linia nie znaleziona"}), 404
    
    line_info = bus_lines[line_number]
    if stop_id not in line_info["stops"]:
        return jsonify({"error": "Przystanek nie znaleziony"}), 404
    
    stop_info = line_info["stops"][stop_id]
    
    # Pobiera odjazdy
    departures = get_departures_for_day(line_number, stop_id)
    next_departures = get_next_departures(departures)
    
    return jsonify({
        "line_number": line_number,
        "line_name": line_info["name"],
        "line_color": line_info["color"],
        "stop_name": stop_info["name"],
        "next_departures": next_departures[:3],
        "all_departures": departures
    })

@app.route('/api/stops')
def get_stops():
    """Zwraca listę wszystkich przystanków - DEPRECATED, używaj /api/lines"""
    all_stops = []
    for line_num, line_data in bus_lines.items():
        for stop_id, stop_data in line_data["stops"].items():
            all_stops.append({"id": f"{line_num}_{stop_id}", "name": f"L{line_num}: {stop_data['name']}"})
    return jsonify(all_stops)

@app.route('/api/legend')
def get_legend():
    """Zwraca legendę przystanków"""
    legend = {
        "date": datetime.now().strftime("%A, %d-%m-%Y"),
        "line_info": {
            "1": "Linia 1: Michałowo pętla ↔ Grunwald pętla",
            "2": "Linia 2: Saminex pętla ↔ Wapna pętla", 
            "3": "Linia 3: Wyspiańskiego ↔ Łyskowskiego pętla",
            "4": "Linia 4: Saminex pętla ↔ Wyspiańskiego",
            "5": "Linia 5: Saminex pętla ↔ Matejki"
        },
        "features": {
            "Planowanie tras": "Wybierz przystanek startowy i docelowy",
            "Rzeczywiste rozkłady": "Aktualne godziny odjazdów autobusów",
            "Szczegółowe trasy": "Rozwiń trasę aby zobaczyć wszystkie przystanki",
            "Asystent AI": "Zapytaj chatbota o połączenia autobusowe"
        },
        "technical_info": {
            "Odświeżanie": "Dane aktualizowane co 30 sekund",
            "Dokładność": "Czasy mogą się różnić o ±2 minuty",
            "Obsługa": "Działa na komputerze i telefonie"
        },
        "note": "System informacji pasażerskiej - Komunikacja miejska w Brodnicy"
    }
    return jsonify(legend)

@app.route('/api/all-stops')
def get_all_stops():
    """Zwraca listę wszystkich przystanków z wszystkich linii, grupowane po nazwie"""
    all_stops = {}
    
    for line_num, line_data in bus_lines.items():
        for stop_id, stop_data in line_data["stops"].items():
            clean_name = stop_data["name"]
            if " - " in clean_name:
                clean_name = clean_name.split(" - ", 1)[1]
            
            clean_name = clean_name.replace(" (L1)", "").replace(" (L2)", "").replace(" (L3)", "").replace(" (L4)", "").replace(" (L5)", "")
            
            if clean_name not in all_stops:
                all_stops[clean_name] = {
                    "id": clean_name.lower().replace(" ", "_").replace("ą", "a").replace("ć", "c").replace("ę", "e").replace("ł", "l").replace("ń", "n").replace("ó", "o").replace("ś", "s").replace("ź", "z").replace("ż", "z"),
                    "name": clean_name,
                    "lines": [],
                    "stop_ids": []  
                }
        
            line_exists = any(line["number"] == line_num for line in all_stops[clean_name]["lines"])
            if not line_exists:
                all_stops[clean_name]["lines"].append({
                    "number": line_num,
                    "color": line_data["color"]
                })
            
            all_stops[clean_name]["stop_ids"].append({
                "line": line_num,
                "stop_id": stop_id
            })
    
    sorted_stops = sorted(all_stops.values(), key=lambda x: x["name"])
    
    return jsonify(sorted_stops)

@app.route('/api/routes/<from_stop>/<to_stop>')
def find_routes(from_stop, to_stop):
    """Znajduje wszystkie autobusy, które mogą zawieźć z przystanku A do B"""
    if from_stop == to_stop:
        return jsonify({"error": "Przystanek startowy i docelowy nie mogą być takie same"}), 400
    
    routes = []
    
    from_stop_ids = []
    to_stop_ids = []
    
    for line_num, line_data in bus_lines.items():
        for stop_id, stop_data in line_data["stops"].items():
            clean_name = stop_data["name"]
            if " - " in clean_name:
                clean_name = clean_name.split(" - ", 1)[1]
            clean_name = clean_name.replace(" (L1)", "").replace(" (L2)", "").replace(" (L3)", "").replace(" (L4)", "").replace(" (L5)", "")
            clean_id = clean_name.lower().replace(" ", "_").replace("ą", "a").replace("ć", "c").replace("ę", "e").replace("ł", "l").replace("ń", "n").replace("ó", "o").replace("ś", "s").replace("ź", "z").replace("ż", "z")
            
            if clean_id == from_stop:
                from_stop_ids.append({"line": line_num, "stop_id": stop_id, "name": clean_name})
            if clean_id == to_stop:
                to_stop_ids.append({"line": line_num, "stop_id": stop_id, "name": clean_name})
    
    if not from_stop_ids or not to_stop_ids:
        return jsonify({
            "error": "Przystanek nie znaleziony",
            "message": "Jeden z wybranych przystanków nie został znaleziony."
        }), 404
    
    for line_num, line_data in bus_lines.items():
        stops_list = list(line_data["stops"].keys())
        
        from_stops_on_line = [fs for fs in from_stop_ids if fs["line"] == line_num]
        to_stops_on_line = [ts for ts in to_stop_ids if ts["line"] == line_num]
        
        for from_stop_data in from_stops_on_line:
            for to_stop_data in to_stops_on_line:
                from_stop_id = from_stop_data["stop_id"]
                to_stop_id = to_stop_data["stop_id"]
                
                if from_stop_id in stops_list and to_stop_id in stops_list:
                    from_index = stops_list.index(from_stop_id)
                    to_index = stops_list.index(to_stop_id)
                    
                    if from_index < to_index:
                        from_stop_info = line_data["stops"][from_stop_id]
                        to_stop_info = line_data["stops"][to_stop_id]
                        
                        departures = get_departures_for_day(line_num, from_stop_id)
                        next_departures = get_next_departures(departures)
                        
                        routes.append({
                            "line_number": line_num,
                            "line_name": line_data["name"],
                            "line_color": line_data["color"],
                            "from_stop": {
                                "id": from_stop_id,
                                "name": from_stop_data["name"],
                                "departures": departures,
                                "next_departures": next_departures[:3]
                            },
                            "to_stop": {
                                "id": to_stop_id,
                                "name": to_stop_data["name"]
                            },
                            "stops_between": to_index - from_index - 1,
                            "estimated_travel_time": (to_index - from_index) * 3
                        })
    
    if not routes:
        return jsonify({
            "error": "Brak bezpośrednich połączeń",
            "message": "Nie znaleziono autobusu, który jedzie bezpośrednio z tego przystanku do wybranego celu."
        }), 404
    
    routes.sort(key=lambda x: x["from_stop"]["next_departures"][0]["minutes_until"] if x["from_stop"]["next_departures"] else 999)
    
    return jsonify({
        "from_stop_name": routes[0]["from_stop"]["name"] if routes else "",
        "to_stop_name": routes[0]["to_stop"]["name"] if routes else "",
        "routes": routes,
        "total_options": len(routes)
    })

@app.route('/api/route-details/<line_number>/<from_stop_id>/<to_stop_id>')
def get_route_details(line_number, from_stop_id, to_stop_id):
    """Zwraca szczegółową trasę z wszystkimi przystankami i czasami"""
    if line_number not in bus_lines:
        return jsonify({"error": "Linia nie znaleziona"}), 404
    
    line_data = bus_lines[line_number]
    
    if 'position' in list(line_data["stops"].values())[0]:
        stops_with_positions = [(stop_id, stop_data["position"]) for stop_id, stop_data in line_data["stops"].items()]
        stops_with_positions.sort(key=lambda x: x[1])
        stops_list = [stop_id for stop_id, _ in stops_with_positions]
    else:
        stops_list = list(line_data["stops"].keys())
    
    if from_stop_id not in stops_list or to_stop_id not in stops_list:
        return jsonify({"error": "Przystanek nie znaleziony"}), 404
    
    from_index = stops_list.index(from_stop_id)
    to_index = stops_list.index(to_stop_id)
    
    if from_index >= to_index:
        return jsonify({"error": "Nieprawidłowy kierunek jazdy"}), 400

    departures = get_departures_for_day(line_number, from_stop_id)
    next_departures = get_next_departures(departures)
    
    if not next_departures:
        return jsonify({"error": "Brak odjazdów"}), 404
    
    departure_time = next_departures[0]["time"]
    departure_hour, departure_minute = map(int, departure_time.split(':'))
    departure_total_minutes = departure_hour * 60 + departure_minute
    
    route_stops = []
    for i in range(from_index, to_index + 1):
        stop_id = stops_list[i]
        stop_data = line_data["stops"][stop_id]
        
        minutes_from_start = (i - from_index) * 3
        arrival_total_minutes = departure_total_minutes + minutes_from_start
        
        if arrival_total_minutes >= 24 * 60:
            arrival_total_minutes -= 24 * 60
        
        arrival_hour = arrival_total_minutes // 60
        arrival_minute = arrival_total_minutes % 60
        arrival_time = f"{arrival_hour:02d}:{arrival_minute:02d}"
        
        clean_name = stop_data["name"]
        if " - " in clean_name:
            clean_name = clean_name.split(" - ", 1)[1]
        clean_name = clean_name.replace(" (L1)", "").replace(" (L2)", "").replace(" (L3)", "").replace(" (L4)", "").replace(" (L5)", "")
        
        route_stops.append({
            "stop_id": stop_id,
            "name": clean_name,
            "arrival_time": arrival_time,
            "minutes_from_start": minutes_from_start,
            "is_origin": i == from_index,
            "is_destination": i == to_index,
            "is_intermediate": from_index < i < to_index
        })
    
    return jsonify({
        "line_number": line_number,
        "line_name": line_data["name"],
        "line_color": line_data["color"],
        "departure_time": departure_time,
        "total_travel_time": (to_index - from_index) * 3,
        "total_stops": len(route_stops),
        "route_stops": route_stops
    })

def get_schedule_context():
    """Przygotowuje kontekst rozkładu jazdy dla AI"""
    current_time = datetime.now().strftime("%H:%M")
    current_date = datetime.now().strftime("%A, %d-%m-%Y")
    
    context = {
        "current_time": current_time,
        "current_date": current_date,
        "available_lines": {},
        "stops": []
    }
    
    for line_num, line_data in bus_lines.items():
        context["available_lines"][line_num] = {
            "name": line_data["name"],
            "stops": []
        }
        

        for stop_id, stop_data in line_data["stops"].items():
            clean_name = stop_data["name"]
            if " - " in clean_name:
                clean_name = clean_name.split(" - ", 1)[1]
            context["available_lines"][line_num]["stops"].append(clean_name)
 
        if line_num == "1" and "stops" in line_data:
            michalowo_stop = line_data["stops"].get("michałowo_petla")
            if michalowo_stop and "departures" in michalowo_stop:
                context["line_1_schedule"] = {
                    "michalowo_petla": michalowo_stop["departures"][:8]  
                }
    
    all_stops = set()
    for line_data in bus_lines.values():
        for stop_data in line_data["stops"].values():
            clean_name = stop_data["name"]
            if " - " in clean_name:
                clean_name = clean_name.split(" - ", 1)[1]
            all_stops.add(clean_name)
    
    context["stops"] = sorted(list(all_stops))[:20]  
    
    return context

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    """Endpoint dla chatbota AI"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "Brak wiadomości"}), 400
        

        context = get_schedule_context()
    
        system_prompt = f"""Jesteś pomocnym asystentem komunikacji miejskiej w Brodnicy, Kujawsko-Pomorskie.

AKTUALNE INFORMACJE:
- Data i czas: {context['current_date']}, godz. {context['current_time']}
- Dostępne linie autobusowe: {', '.join(context['available_lines'].keys())}

LINIE AUTOBUSOWE:
Linia 1: Michałowo pętla ↔ Grunwald pętla
Linia 2: Saminex pętla ↔ Wapna pętla
Linia 3: Wyspiańskiego ↔ Łyskowskiego pętla
Linia 4: Saminex pętla ↔ Wyspiańskiego
Linia 5: Saminex pętla ↔ Matejki

ROZKŁAD LINII 1 (z Michałowo pętla):
{context.get('line_1_schedule', {}).get('michalowo_petla', ['Brak danych'])}

GŁÓWNE PRZYSTANKI:
Michałowo pętla, Grunwald pętla, Saminex pętla, Wyspiańskiego, Dworzec, Rynek, Matejki, Przykop, Mazurska, Wapna pętla, Łyskowskiego pętla

ZASADY ODPOWIEDZI:
1. Odpowiadaj TYLKO po polsku
2. Bądź konkretny i pomocny
3. Podawaj dokładne godziny w formacie HH:MM
4. Jeśli nie masz dokładnych danych, zasugeruj sprawdzenie na stronie
5. Używaj emoji: 🚌 ⏰ 📍 🔄
6. Odpowiadaj krótko (max 2-3 zdania)
7. Jeśli pytanie dotyczy tras, wskaż odpowiednią linię

PRZYKŁADY DOBRYCH ODPOWIEDZI:
- "🚌 Autobus linii 1 z Michałowo jedzie o: 06:30, 07:00, 07:30..."
- "📍 Do Grunwalda jedzie linia 1 z Michałowo pętla"
- "⏰ Następny autobus za około X minut"

Bądź przyjazny ale profesjonalny. Jeśli nie wiesz czegoś dokładnie, powiedz to wprost."""

        response = ollama.chat(
            model='llama3.2:latest',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            options={
                "temperature": 0.1,  # Bardzo mało kreatywności, więcej faktów
                "top_p": 0.8,
                "num_ctx": 4096,    # Większy kontekst
                "repeat_penalty": 1.1,
                "num_predict": 150   # Ograniczenie długości odpowiedzi
            }
        )
        
        ai_response = response['message']['content'].strip()
        
        return jsonify({
            "response": ai_response,
            "timestamp": datetime.now().isoformat(),
            "context_used": {
                "current_time": context['current_time'],
                "day_type": context['current_day']
            }
        })
        
    except Exception as e:
        print(f"Błąd AI: {e}")
        return jsonify({
            "error": "Nie mogę teraz odpowiedzieć. Spróbuj ponownie.",
            "response": "🚌 Przepraszam, mam problem z połączeniem. Sprawdź rozkład ręcznie lub spróbuj ponownie za chwilę."
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
