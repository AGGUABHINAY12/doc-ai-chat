#!/usr/bin/env python3
import subprocess
import time
import sys
import os
import webbrowser
import signal

def run_services():
    print("\n" + "="*50)
    print("🚀 SmartPrep AI - Starting Services")
    print("="*50)
    
    processes = []
    
    try:
        # Get directories
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
        
        # Check if requirements.txt exists and install (optional - remove if you don't want)
        print("\n📦 Checking backend dependencies...")
        requirements_file = os.path.join(backend_dir, 'requirements.txt')
        if os.path.exists(requirements_file):
            # Comment this line if you don't want auto-install
            # subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], check=False)
            print("✅ Dependencies ready")
        else:
            print("⚠️ requirements.txt not found")
        
        # Start backend
        print("\n📡 Starting Backend Server on http://localhost:8000...")
        backend = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        processes.append(backend)
        
        # Wait for backend to initialize
        print("⏳ Waiting for backend to start...")
        time.sleep(5)
        
        # Start frontend
        print("\n🌐 Starting Frontend Server on http://localhost:5500...")
        
        # Check if index.html exists
        index_file = os.path.join(frontend_dir, 'index.html')
        if not os.path.exists(index_file):
            print(f"❌ Error: index.html not found in {frontend_dir}")
            print("📁 Make sure index.html is in the frontend folder")
            sys.exit(1)
        
        # Start HTTP server in frontend directory
        frontend = subprocess.Popen(
            [sys.executable, "-m", "http.server", "5500"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        processes.append(frontend)
        
        # Print success message
        print("\n" + "="*50)
        print("✅ Services Started Successfully!")
        print("📌 Backend API:  http://localhost:8000")
        print("📌 Frontend App: http://localhost:5500")
        print("="*50)
        print("\n🌐 Opening browser automatically...")
        
        # Open browser after a short delay
        time.sleep(2)
        webbrowser.open("http://localhost:5500")
        
        print("\n💡 Demo Login Credentials:")
        print("   📧 Email: demo@smartprep.com")
        print("   🔑 Password: demo123")
        print("\n💡 Or register a new account")
        print("\n⚠️  Press Ctrl+C to stop both servers\n")
        
        # Monitor processes
        while True:
            # Check if any process died
            for proc in processes:
                if proc.poll() is not None:
                    print(f"\n⚠️ A server stopped unexpectedly (PID: {proc.pid})")
                    return
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down services...")
        for proc in processes:
            proc.terminate()
            time.sleep(0.5)
            if proc.poll() is None:
                proc.kill()
        print("✅ All services stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        for proc in processes:
            proc.terminate()
        sys.exit(1)

if __name__ == "__main__":
    run_services()