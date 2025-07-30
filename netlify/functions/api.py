import json
import sqlite3
import os
from datetime import datetime
import random

def generate_character_from_ingredients(ingredients):
    """成分データからキャラクターの能力値を計算"""
    total_protein = sum(ing.get('protein', 0) for ing in ingredients)
    total_fat = sum(ing.get('fat', 0) for ing in ingredients)
    total_carbs = sum(ing.get('carbs', 0) for ing in ingredients)
    total_sugar = sum(ing.get('sugar', 0) for ing in ingredients)
    total_salt = sum(ing.get('salt', 0) for ing in ingredients)
    
    # 能力値計算
    hp = 100 + (total_protein * 2)
    attack = 50 + (total_fat * 3)
    defense = 30 + (total_carbs * 2)
    speed = 20 + (total_sugar * 5)
    
    # キャラクター名生成
    names = ["栄養戦士", "成分騎士", "健康勇者", "バランス戦士", "栄養の守護者"]
    name = names[hash(str(ingredients)) % len(names)]
    
    return {
        'name': name,
        'hp': hp,
        'attack': attack,
        'defense': defense,
        'speed': speed,
        'ingredients': ingredients
    }

def get_sample_characters():
    """サンプルキャラクターを生成"""
    return [
        {
            'name': '栄養戦士',
            'level': 5, 'exp': 150, 'hp': 180, 'attack': 85, 'defense': 70, 'speed': 45
        },
        {
            'name': '成分騎士',
            'level': 3, 'exp': 80, 'hp': 140, 'attack': 65, 'defense': 55, 'speed': 35
        },
        {
            'name': '健康勇者',
            'level': 7, 'exp': 220, 'hp': 200, 'attack': 95, 'defense': 80, 'speed': 50
        }
    ]

def handler(event, context):
    """Netlify Functions ハンドラー"""
    path = event.get('path', '')
    method = event.get('httpMethod', 'GET')
    
    # CORS ヘッダー
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Content-Type': 'application/json'
    }
    
    # OPTIONS リクエスト（CORS preflight）
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    # API ルーティング
    if path == '/api/analyze_ingredients' and method == 'POST':
        try:
            body = json.loads(event.get('body', '{}'))
            ingredients = body.get('ingredients', [])
            character = generate_character_from_ingredients(ingredients)
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'success': True,
                    'character': character
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({'error': str(e)})
            }
    
    elif path == '/api/battle' and method == 'POST':
        try:
            body = json.loads(event.get('body', '{}'))
            player_character = body.get('player_character', {})
            opponent_character = body.get('opponent_character', {})
            
            # シンプルなバトルロジック
            player_power = player_character.get('attack', 0) + player_character.get('speed', 0)
            opponent_power = opponent_character.get('attack', 0) + opponent_character.get('speed', 0)
            
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
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'success': True,
                    'result': result,
                    'exp_gained': exp_gained,
                    'battle_log': [
                        f"{player_character.get('name', 'プレイヤー')}の攻撃力: {player_power} + {player_roll} = {player_total}",
                        f"{opponent_character.get('name', '敵')}の攻撃力: {opponent_power} + {opponent_roll} = {opponent_total}",
                        f"結果: {'勝利' if result == 'win' else '敗北' if result == 'lose' else '引き分け'}"
                    ]
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({'error': str(e)})
            }
    
    elif path == '/api/characters' and method == 'GET':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'characters': []})
        }
    
    elif path == '/api/sample_characters' and method == 'GET':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'characters': get_sample_characters()})
        }
    
    else:
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({'error': 'Not found'})
        } 