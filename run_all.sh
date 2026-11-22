#!/bin/zsh
# Lance chaque programme du livre avec des réponses déjà tapées, et indique lesquels marchent.
# Utilisation (depuis le dossier du code, avec le venv activé) :  ./run_all.sh
# Les programmes qui ont besoin d’une clé Groq ou de PostgreSQL sont sautés s’ils manquent.
cd "${0:A:h}"
PY="${PYTHON:-python}"
KEEP_PG="$POSTGRES_URL"
[[ -f .env ]] && set -a && source .env && set +a
[[ -n "$KEEP_PG" ]] && export POSTGRES_URL="$KEEP_PG"  # une URL donnée en ligne de commande l’emporte
export TRANSFORMERS_VERBOSITY=error TOKENIZERS_PARALLELISM=false
LOG="run_all.log"; : > "$LOG"
pass=0; fail=0; skip=0

run() {  # run <besoin : none|llm|pg> <script> <saisie tapée>
  local needs=$1 script=$2 input=$3
  if [[ $needs == llm* && -z "$GROQ_API_KEY" ]]; then echo "⏭  $script (no GROQ_API_KEY)"; ((skip++)); return; fi
  if [[ $needs == *pg && -z "$PG_OK" ]]; then echo "⏭  $script (no PostgreSQL)"; ((skip++)); return; fi
  [[ $needs == llm* ]] && sleep 8  # rester sous la limite de tokens par minute de l’offre gratuite
  echo "\n===== $script" >> "$LOG"
  if print -r -- "$input" | "$PY" "$script" >> "$LOG" 2>&1; then echo "✅ $script"; ((pass++))
  else echo "❌ $script (see $LOG)"; ((fail++)); fi
}

"$PY" -c "import os,psycopg; psycopg.connect(os.getenv('POSTGRES_URL','postgresql://postgres:comet@localhost:5432/postgres')).close()" 2>/dev/null && PG_OK=1

run none 00_boarding/survival_kit.py ""
run none 00_boarding/hello_check.py ""
run none 00_boarding/order_taker.py $'Espresso\nCroissant\ndone'
run llm  01_chatbot/first_call_hf.py ""
run llm  01_chatbot/first_call_wrapper.py ""
run llm  01_chatbot/chat_v1.py $'Hi, I am Marta.\nWhat is my name?\nbye'
run llm  01_chatbot/chat_v2.py $'Hi, I am Marta.\nWhat is my name?\nbye'
run none 01_chatbot/token_counter.py ""
run none 01_chatbot/any_tokenizer.py ""
run llm  01_chatbot/chatbot_oop.py $'Hello!\nWhat do you recommend on a rainy day?\nbye'
run llm  01_chatbot/chatbot.py $'Hi, I am Marta and I love cappuccino.\nTell me a long story about a comet that visits a café.\nNow another story, about a croissant astronaut.\nAnd one about a dog called Pixel.\nWhat is my name and favourite drink?\nbye'
run llm  02_classifier/review_sorter_llm.py ""
run none 02_classifier/nli_demo.py ""
run none 02_classifier/review_sorter_local.py ""
run none 03_embeddings/embeddings_demo.py ""
run none 03_embeddings/menu_search.py ""
run none 04_rag/build_library.py ""
run llm  04_rag/ask_handbook.py $'Can I bring my dog?\nIs the brownie nut-free?\nWhat is the wifi password?\nbye'
run llm  05_agent/lc_chat.py $'Hi, I am Jules.\nWhat is my name?\nbye'
run llm  05_agent/manual_agent.py ""
run llm  05_agent/weather_agent.py ""
run llm  05_agent/graph_agent.py ""
run llm  05_agent/supplier_search_agent.py "price of organic oat milk for cafés in France"
run llm  05_agent/mcp_agent.py ""
run llm  06_structured/templates_demo.py ""
run llm  06_structured/order_extractor.py ""
run llm  07_memory/nova_memory.py $'Marta\nI love cappuccino.\nswitch\nJules\nWhat do I love?\nswitch\nMarta\nWhat do I love?\nbye'
run llmpg 07_memory/nova_postgres.py $'Priya\nMy favourite cake is the cheesecake.\nbye'
run llmpg 07_memory/nova_postgres.py $'Priya\nWhat is my favourite cake?\nbye'
run pg   07_memory/read_history.py "Priya"
run llm  08_middleware/nova_middleware.py $'Hi, I am Marta, I love cappuccino and I come every Monday.\nTell me about the history of coffee in detail.\nAnd the history of croissants?\nAnd of hot chocolate?\nWhat is my name and when do I come?\nbye'
run none 09_langgraph/first_graph.py ""
run llm  09_langgraph/newsletter_studio.py "our new autumn menu"
run llm  10_multi_agent/cafe_team.py ""
run llm  11_landing/traffic_lights.py $'Marta paid for a Comet Cheesecake that was dry. Refund her the menu price.\nno'
run none mission_log/ch03_order_taker.py $'croissant\nHOT CHOCOLATE\ndone'
run llm  mission_log/ch05_chat_counter.py $'Hello!\nciao'
run llm  mission_log/ch07_reset.py $'Hi, I am Marta.\nreset\nWhat is my name?\nbye'
run llm  mission_log/ch08_both_strategies.py $'Hi, I am Marta.\nTell me a long story about a comet.\nAnother about a croissant.\nAnd one about Pixel the dog.\nWhat is my name?\nbye'
run llm  mission_log/ch09_mixed_label.py ""
run none mission_log/ch10_atmosphere_topic.py ""
run none mission_log/ch11_ask_the_menu.py $'a caffeine-free hot drink\nbye'
run none mission_log/ch12_handbook_tokens.py ""
run none mission_log/ch13_no_crumbs.py ""
run llm  mission_log/ch14_too_far.py $'Can I bring my dog?\nWhat is the wifi password?\nbye'

run none mission_log/ch15_opening_hours_tool.py ""
run llm  mission_log/ch16_opening_hours_agent.py ""
run llm  mission_log/ch17_allergen_agent.py ""
run llm  mission_log/ch18_welcome_cards.py ""
run llm  mission_log/ch19_pickup_day_and_note.py ""
run pg   mission_log/ch20_count_messages.py "Priya"
run llm  mission_log/ch21_luggage_after.py $'Hi, I am Marta, I love cappuccino and I come every Monday.\nTell me about the history of coffee in detail.\nAnd the history of croissants?\nAnd of hot chocolate?\nWhat is my name and when do I come?\nbye'
run none mission_log/ch22_tea_station.py ""
run llm  mission_log/ch23_word_counter.py "our new autumn menu"
run llm  mission_log/ch24_translator.py ""
run llm  mission_log/ch25_refund_limit.py "Refund Jules 45 euros for a birthday cake."
echo "\n$pass passed, $fail failed, $skip skipped. Full output in $LOG"
[[ $fail -eq 0 ]]
