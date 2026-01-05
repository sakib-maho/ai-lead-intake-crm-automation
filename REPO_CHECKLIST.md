# Repository Checklist - What Should Be Pushed

## ✅ Core Application Files

- [x] `app/main.py` - FastAPI application
- [x] `app/ai.py` - OpenAI integration
- [x] `app/schemas.py` - Pydantic models
- [x] `app/utils.py` - Validation & utilities
- [x] `app/settings.py` - Configuration
- [x] `app/__init__.py` - Package init

## ✅ Website Files

- [x] `website/index.html` - Contact form
- [x] `website/README.md` - Website setup guide
- [x] `website/TROUBLESHOOTING.md` - Troubleshooting guide
- [x] `website/FIX_WEBHOOK_410.md` - Webhook fix guide

## ✅ Documentation

- [x] `README.md` - Main project documentation
- [x] `make/scenario_blueprint.md` - Make.com setup
- [x] `make/prompts.md` - OpenAI prompts
- [x] `make/data_mapping.md` - Google Sheets mapping
- [x] `SETUP_MAKECOM_LOCAL.md` - Local setup guide
- [x] `MAKECOM_SETUP_STEPS.md` - Step-by-step guide
- [x] `PUSH_TO_GITHUB.md` - GitHub push instructions

## ✅ Configuration & Scripts

- [x] `requirements.txt` - Python dependencies
- [x] `requirements-py314.txt` - Python 3.14 version
- [x] `.gitignore` - Git ignore rules
- [x] `setup.sh` - Setup script
- [x] `setup_py314.sh` - Python 3.14 setup
- [x] `setup_ngrok_auth.sh` - ngrok auth setup
- [x] `setup_git_repo.sh` - Git repo setup
- [x] `start_ngrok.sh` - Start ngrok tunnel
- [x] `run.sh` - Run server script
- [x] `kill_port.sh` - Kill process on port
- [x] `test_makecom_webhook.sh` - Test webhook script
- [x] `verify_repo.sh` - Verify repository script

## ✅ Examples

- [x] `examples/sample_lead.json` - Sample payload
- [x] `examples/curl_test.sh` - Test script

## ✅ Other Files

- [x] `FIX_PYTHON314.md` - Python 3.14 fix guide
- [x] `REPO_CHECKLIST.md` - This file

## ❌ Should NOT Be Pushed (Protected by .gitignore)

- [ ] `.env` - Contains API keys (SENSITIVE!)
- [ ] `venv/` - Virtual environment
- [ ] `__pycache__/` - Python cache
- [ ] `*.pyc` - Compiled Python
- [ ] `MAKECOM_URL.txt` - Contains webhook URLs
- [ ] `check_env.py` - Temporary script
- [ ] `.DS_Store` - macOS files

## Quick Verification Commands

```bash
# Check what's tracked
git ls-files

# Check what's NOT tracked (should include .env, venv)
git status

# Verify sensitive files are ignored
git check-ignore .env venv/

# See commit history
git log --oneline

# Check remote (if pushed)
git remote -v
```

## If Something is Missing

```bash
# Add missing files
git add <file>

# Commit
git commit -m "Add missing files"

# Push
git push
```

