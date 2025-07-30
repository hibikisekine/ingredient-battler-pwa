from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
import json
import os
from datetime import datetime

app = Flask(__name__)

# データベース初期化
def init_db():
    conn = sqlite3.connect('ingredient_battler.db')
    cursor = conn.cursor()
    
    # ユーザーテーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # キャラクターテーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            name TEXT NOT NULL,
            ingredient_data TEXT,
            level INTEGER DEFAULT 1,
            exp INTEGER DEFAULT 0,
            hp INTEGER DEFAULT 100,
            attack INTEGER DEFAULT 50,
            defense INTEGER DEFAULT 30,
            speed INTEGER DEFAULT 20,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # バトル履歴テーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS battles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            character_id INTEGER,
            opponent_name TEXT,
            result TEXT,
            exp_gained INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (character_id) REFERENCES characters (id)
        )
    ''')
    
    # デフォルトユーザーを作成
    cursor.execute('''
        INSERT OR IGNORE INTO users (id, username) VALUES (1, 'default_user')
    ''')
    
    conn.commit()
    conn.close()

# 成分からキャラクター生成
def generate_character_from_ingredients(ingredients):
    """成分データからキャラクターの能力値を計算"""
    total_protein = sum(ing.get('protein', 0) for ing in ingredients)
    total_fat = sum(ing.get('fat', 0) for ing in ingredients)
    total_carbs = sum(ing.get('carbs', 0) for ing in ingredients)
    total_sugar = sum(ing.get('sugar', 0) for ing in ingredients)
    total_salt = sum(ing.get('salt', 0) for ing in ingredients)
    
    # 能力値計算
    hp = 100 + (total_protein * 2)  # タンパク質でHP増加
    attack = 50 + (total_fat * 3)   # 脂質で攻撃力増加
    defense = 30 + (total_carbs * 2) # 炭水化物で防御力増加
    speed = 20 + (total_sugar * 5)   # 糖質でスピード増加
    
    # キャラクター名生成
    names = ["栄養戦士", "成分騎士", "健康勇者", "バランス戦士", "栄養の守護者", 
             "タンパク質戦士", "脂質騎士", "炭水化物勇者", "糖質戦士", "塩分の守護者"]
    name = names[hash(str(ingredients)) % len(names)]
    
    return {
        'name': name,
        'hp': hp,
        'attack': attack,
        'defense': defense,
        'speed': speed,
        'ingredients': ingredients
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('.', 'manifest.json')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/api/analyze_ingredients', methods=['POST'])
def analyze_ingredients():
    """OCRで読み取った成分データを処理"""
    data = request.get_json()
    ingredients = data.get('ingredients', [])
    
    # キャラクター生成
    character = generate_character_from_ingredients(ingredients)
    
    # データベースに保存
    save_character_to_db(character)
    
    return jsonify({
        'success': True,
        'character': character
    })

def save_character_to_db(character):
    """キャラクターをデータベースに保存"""
    conn = sqlite3.connect('ingredient_battler.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO characters (user_id, name, ingredient_data, hp, attack, defense, speed)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            1,  # デフォルトユーザーID
            character['name'],
            json.dumps(character.get('ingredients', [])),
            character['hp'],
            character['attack'],
            character['defense'],
            character['speed']
        ))
        
        conn.commit()
        print(f"キャラクター '{character['name']}' を保存しました")
        
    except Exception as e:
        print(f"キャラクター保存エラー: {e}")
    finally:
        conn.close()

@app.route('/api/battle', methods=['POST'])
def battle():
    """バトル処理"""
    data = request.get_json()
    player_character = data.get('player_character')
    opponent_character = data.get('opponent_character')
    
    # シンプルなバトルロジック
    player_power = player_character['attack'] + player_character['speed']
    opponent_power = opponent_character['attack'] + opponent_character['speed']
    
    # ランダム要素を加える
    import random
    player_roll = random.randint(1, 20)
    opponent_roll = random.randint(1, 20)
    
    player_total = player_power + player_roll
    opponent_total = opponent_power + opponent_roll
    
    if player_total > opponent_total:
        result = 'win'
        exp_gained = 10
    elif player_total < opponent_total:
        result = 'lose'
        exp_gained = 5
    else:
        result = 'draw'
        exp_gained = 7
    
    return jsonify({
        'success': True,
        'result': result,
        'exp_gained': exp_gained,
        'battle_log': [
            f"{player_character['name']}の攻撃力: {player_power} + {player_roll} = {player_total}",
            f"{opponent_character['name']}の攻撃力: {opponent_power} + {opponent_roll} = {opponent_total}",
            f"結果: {'勝利' if result == 'win' else '敗北' if result == 'lose' else '引き分け'}"
        ]
    })

@app.route('/api/characters', methods=['GET'])
def get_characters():
    """ユーザーのキャラクター一覧を取得"""
    conn = sqlite3.connect('ingredient_battler.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT id, name, level, exp, hp, attack, defense, speed, created_at 
            FROM characters 
            ORDER BY created_at DESC
        ''')
        
        characters = []
        for row in cursor.fetchall():
            characters.append({
                'id': row[0],
                'name': row[1],
                'level': row[2],
                'exp': row[3],
                'hp': row[4],
                'attack': row[5],
                'defense': row[6],
                'speed': row[7],
                'created_at': row[8]
            })
        
        return jsonify({'characters': characters})
        
    except Exception as e:
        print(f"キャラクター取得エラー: {e}")
        return jsonify({'characters': []})
    finally:
        conn.close()

@app.route('/api/sample_characters', methods=['GET'])
def get_sample_characters():
    """サンプルキャラクターを生成"""
    sample_characters = [
        {
            'name': '栄養戦士',
            'level': 5,
            'exp': 150,
            'hp': 180,
            'attack': 85,
            'defense': 70,
            'speed': 45
        },
        {
            'name': '成分騎士',
            'level': 3,
            'exp': 80,
            'hp': 140,
            'attack': 65,
            'defense': 55,
            'speed': 35
        },
        {
            'name': '健康勇者',
            'level': 7,
            'exp': 220,
            'hp': 200,
            'attack': 95,
            'defense': 80,
            'speed': 50
        },
        {
            'name': 'バランス戦士',
            'level': 4,
            'exp': 100,
            'hp': 160,
            'attack': 75,
            'defense': 65,
            'speed': 40
        },
        {
            'name': '栄養の守護者',
            'level': 6,
            'exp': 180,
            'hp': 190,
            'attack': 90,
            'defense': 75,
            'speed': 48
        }
    ]
    
    return jsonify({'characters': sample_characters})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001) 