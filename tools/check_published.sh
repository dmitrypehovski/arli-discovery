#!/usr/bin/env bash
# Проверка того, что опубликовано: сравнить то, что отдаёт наш домен, с тем, что лежит здесь.
#
# Зачем отдельный скрипт. Публикация это не событие, а состояние: файл мог уплыть, правило
# могло отвалиться, копия на домене могла остаться от прежней версии. Проверка занимает
# секунды и отвечает на вопрос «то, что мы обещаем адресом, действительно там».
#
# Запуск: bash tools/check_published.sh
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STATUS=0

check() {
  local name="$1" url="$2" local_file="$3"
  if [ -z "$local_file" ]; then
    # Адресам без местного файла довольно кода ответа: содержимое двоичное.
    local code
    code="$(curl -fsS -o /dev/null -w '%{http_code}' "$url" 2>/dev/null)" || code="000"
    if [ "$code" = "200" ]; then
      echo "отвечает: $name ($url)"
    else
      echo "не отвечает: $name ($url), код $code"
      STATUS=1
    fi
    return
  fi
  local got
  got="$(curl -fsS "$url" 2>/dev/null)" || { echo "не отвечает: $name ($url)"; STATUS=1; return; }
  if [ "$got" = "$(cat "$local_file")" ]; then
    echo "совпадает: $name"
  else
    echo "РАСХОЖДЕНИЕ: $name ($url) не равен $local_file"
    STATUS=1
  fi
}

check "страница текста" "https://arliwork.com/spec/index.html" "$ROOT/docs/spec.html"
check "определение расширения" "https://arliwork.com/a2a/extensions/arli.discovery.v1" "$ROOT/docs/extension-definition.json"
check "зеркало репозитория" "https://arliwork.com/plugin/arli-spec.git/info/refs?service=git-upload-pack" ""
check "площадка кода" "https://api.github.com/repos/dmitrypehovski/arli-discovery" ""

if [ "$STATUS" -eq 0 ]; then
  echo "итог: опубликованное совпадает с собранным"
else
  echo "итог: есть расхождения, публикацию надо повторить"
fi
exit "$STATUS"
