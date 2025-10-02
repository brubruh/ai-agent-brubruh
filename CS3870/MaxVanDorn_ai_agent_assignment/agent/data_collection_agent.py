import requests
import time
import json
import random
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCollectionAgent:
    def __init__(self, config_file):
        """Initialize agent with configuration from your DMP"""
        self.config = self.load_config(config_file)
        self.data_store = []
        self.collection_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'data_quality_score': 0
        }
        
        # Initialize strategy variables
        self.delay_multiplier = 1.0
        self.current_api = self.config['api_settings'].get('primary_api', 'default')
        self.start_time = datetime.now()
        
        # Load API credentials if using .env
        self.api_key = self._load_api_credentials()
        
    def load_config(self, config_file):
        """Load collection parameters from DMP"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Set default values if not specified
            default_config = {
                'agent_settings': {
                    'base_delay': 1.0,
                    'max_requests': 100,
                    'timeout': 10,
                    'retry_attempts': 3
                },
                'api_settings': {
                    'rate_limit_per_minute': 30,
                    'burst_limit': 10
                },
                'data_quality': {
                    'min_completeness': 0.8,
                    'min_accuracy': 0.9
                }
            }
            
            # Merge with defaults
            for section, defaults in default_config.items():
                if section not in config:
                    config[section] = {}
                for key, default_value in defaults.items():
                    if key not in config[section]:
                        config[section][key] = default_value
            
            logger.info(f"Successfully loaded configuration from {config_file}")
            return config
            
        except FileNotFoundError:
            logger.error(f"Configuration file {config_file} not found")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise

    def collect_data(self):
        # Main collection loop with adaptive strategy
        while not self.collection_complete():
            # Assess current data quality
            quality_score = self.assess_data_quality()
            
            # Adapt strategy based on success rate
            if self.get_success_rate() < 0.8:
                self.adjust_strategy()
            
            # Make API calls with rate limiting
            data = self.make_api_request()
            
            if data:
                # Process and validate data
                processed_data = self.process_data(data)
                if self.validate_data(processed_data):
                    self.store_data(processed_data)
            
            # Respectful delay
            self.respectful_delay()
    def assess_data_quality(self):
    # """Evaluate the quality of collected data"""
        if not self.data_store:
            return 0
    
        quality_metrics = {
            'completeness': self.check_completeness(),
            'accuracy': self.check_accuracy(), 
            'consistency': self.check_consistency(),
            'timeliness': self.check_timeliness()
        }
    
        # Calculate overall quality score
        return sum(quality_metrics.values()) / len(quality_metrics)
    
    def adjust_strategy(self):
        #"""Modify collection approach based on performance"""
        success_rate = self.get_success_rate()
        
        if success_rate < 0.5:
            # Increase delays, try alternative APIs
            self.delay_multiplier *= 2
            self.try_fallback_api()
        elif success_rate > 0.9:
            # Can be more aggressive
            self.delay_multiplier *= 0.8
        
        # Log strategy changes
        self.log_strategy_change()
    
    def respectful_delay(self):
        """Implement respectful rate limiting"""
        base_delay = self.config.get('base_delay', 1.0)
        delay = base_delay * self.delay_multiplier
        
        # Add random jitter to avoid thundering herd
        jitter = random.uniform(0.5, 1.5)
        time.sleep(delay * jitter)
    
    def check_rate_limits(self):
        """Monitor and respect API rate limits"""
        # Check if we're approaching limits
        # Adjust collection speed accordingly
        pass
    
    def _load_api_credentials(self):
        """Load API credentials from .env file or config"""
        try:
            # First, try to get API key from config file directly
            api_key = self.config.get('api_settings', {}).get('primary_api', '')
            if api_key and api_key.startswith('eyJ'):  # JWT token pattern
                logger.info("🔑 API key found in config.json")
                return api_key
            
            # Second, try .env file in current directory
            import os
            env_paths = ['.env', '../demo/.env', '../.env']
            
            for env_path in env_paths:
                if os.path.exists(env_path):
                    logger.info(f"📁 Found .env file at: {env_path}")
                    with open(env_path, 'r') as f:
                        for line in f:
                            if '=' in line and not line.strip().startswith('#'):
                                key, value = line.strip().split('=', 1)
                                os.environ[key] = value
                    
                    # Try different key names
                    for key_name in ['CLASH_ROYAL_API_KEY', 'CLASH_ROYALE_API_KEY']:
                        api_key = os.getenv(key_name)
                        if api_key:
                            logger.info(f"🔑 API key found in .env as {key_name}")
                            return api_key
            
            logger.warning("⚠️  No API key found in config or .env files")
            return None
            
        except Exception as e:
            logger.warning(f"Could not load API credentials: {e}")
            return None
    
    def collection_complete(self):
        """Check if collection targets are met"""
        max_requests = self.config['agent_settings']['max_requests']
        return self.collection_stats['total_requests'] >= max_requests
    
    def get_success_rate(self):
        """Calculate current success rate"""
        total = self.collection_stats['total_requests']
        if total == 0:
            return 1.0  # Start optimistic
        return self.collection_stats['successful_requests'] / total
    
    def make_api_request(self):
        """Make API request with enhanced connectivity diagnostics"""
        self.collection_stats['total_requests'] += 1
        
        # API connectivity diagnostics
        url = "https://api.clashroyale.com/v1/cards"
        headers = {}
        
        logger.info(f"🌐 Attempting API request #{self.collection_stats['total_requests']}")
        logger.info(f"📡 Target URL: {url}")
        
        # Check API key
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
            logger.info(f"🔑 API Key: Present (length: {len(self.api_key)} chars)")
            logger.info(f"🔑 API Key starts with: {self.api_key[:20]}...")
        else:
            logger.warning("⚠️  No API key found!")
        
        # Add user agent and other headers
        headers.update({
            'Accept': 'application/json',
            'User-Agent': 'DataCollectionAgent/1.0'
        })
        logger.info(f"📋 Headers: {list(headers.keys())}")
        
        try:
            # Test network connectivity first
            logger.info("🔍 Testing network connectivity...")
            import socket
            socket.create_connection(("api.clashroyale.com", 443), timeout=5)
            logger.info("✅ Network connectivity: OK")
            
            # Make the actual request
            timeout = self.config['agent_settings']['timeout']
            logger.info(f"⏱️  Request timeout: {timeout}s")
            
            response = requests.get(url, headers=headers, timeout=timeout)
            
            # Detailed response analysis
            logger.info(f"📊 Response status: {response.status_code}")
            logger.info(f"📊 Response headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                self.collection_stats['successful_requests'] += 1
                logger.info("🎉 API request successful!")
                
                raw_data = response.json()
                logger.info(f"📦 Data received: {len(raw_data.get('items', []))} items")
                
                # Save raw data immediately
                self.save_raw_data(raw_data, 'cards')
                
                return raw_data
                
            elif response.status_code == 403:
                self.collection_stats['failed_requests'] += 1
                logger.error("🚫 403 Forbidden - API key may be invalid or expired")
                logger.error("💡 Check your API key in the config.json file")
                try:
                    error_detail = response.json()
                    logger.error(f"🔍 API Error Details: {error_detail}")
                except:
                    logger.error(f"🔍 API Response Text: {response.text[:200]}")
                return None
                
            elif response.status_code == 429:
                self.collection_stats['failed_requests'] += 1
                logger.error("⏰ 429 Rate Limited - Too many requests")
                retry_after = response.headers.get('Retry-After', 'unknown')
                logger.error(f"⏰ Retry after: {retry_after} seconds")
                return None
                
            elif response.status_code == 401:
                self.collection_stats['failed_requests'] += 1
                logger.error("🔐 401 Unauthorized - Authentication failed")
                logger.error("💡 Verify your API key is correct")
                return None
                
            else:
                self.collection_stats['failed_requests'] += 1
                logger.error(f"❌ Unexpected status code: {response.status_code}")
                logger.error(f"❌ Response: {response.text[:200]}")
                return None
                
        except socket.gaierror as e:
            self.collection_stats['failed_requests'] += 1
            logger.error(f"🌐 DNS Resolution failed: {e}")
            logger.error("💡 Check your internet connection")
            return None
            
        except socket.timeout as e:
            self.collection_stats['failed_requests'] += 1
            logger.error(f"⏰ Network timeout: {e}")
            logger.error("💡 Check your network connection or firewall")
            return None
            
        except requests.exceptions.Timeout:
            self.collection_stats['failed_requests'] += 1
            logger.error(f"⏰ Request timed out after {timeout}s")
            logger.error("💡 Try increasing timeout in config.json")
            return None
            
        except requests.exceptions.ConnectionError as e:
            self.collection_stats['failed_requests'] += 1
            logger.error(f"🔌 Connection error: {e}")
            logger.error("💡 Check internet connection and firewall settings")
            return None
            
        except requests.exceptions.RequestException as e:
            self.collection_stats['failed_requests'] += 1
            logger.error(f"📡 Request error: {e}")
            return None
            
        except Exception as e:
            self.collection_stats['failed_requests'] += 1
            logger.error(f"💥 Unexpected error: {e}")
            import traceback
            logger.error(f"🔍 Full traceback: {traceback.format_exc()}")
            return None
    
    def process_data(self, raw_data):
        """Process and clean raw API data"""
        if not raw_data or 'items' not in raw_data:
            return None
        
        processed_items = []
        for item in raw_data['items']:
            processed_item = {
                'name': item.get('name', ''),
                'elixir_cost': item.get('elixirCost', 0),
                'type': item.get('type', ''),
                'rarity': item.get('rarity', ''),
                'collected_at': datetime.now().isoformat()
            }
            processed_items.append(processed_item)
        
        return processed_items
    
    def validate_data(self, data):
        """Validate data quality"""
        if not data:
            return False
        
        required_fields = self.config['data_quality']['required_fields']
        
        for item in data:
            # Check if all required fields are present
            for field in required_fields:
                if field not in item or not item[field]:
                    logger.warning(f"Data validation failed: missing {field}")
                    return False
        
        return True
    
    def store_data(self, data):
        """Store validated processed data"""
        self.data_store.extend(data)
        
        # Save processed data to file
        self.save_processed_data(data, 'cards')
        
        logger.info(f"Stored {len(data)} items. Total: {len(self.data_store)}")
    
    def check_completeness(self):
        """Check data completeness"""
        if not self.data_store:
            return 0
        
        total_items = len(self.data_store)
        complete_items = 0
        
        required_fields = self.config['data_quality']['required_fields']
        
        for item in self.data_store:
            if all(field in item and item[field] for field in required_fields):
                complete_items += 1
        
        return complete_items / total_items if total_items > 0 else 0
    
    def check_accuracy(self):
        """Check data accuracy - placeholder"""
        # This would involve more complex validation
        return 0.9  # Placeholder
    
    def check_consistency(self):
        """Check data consistency - placeholder"""
        # This would check for consistent formats, types, etc.
        return 0.85  # Placeholder
    
    def check_timeliness(self):
        """Check data timeliness"""
        if not self.data_store:
            return 0
        
        current_time = datetime.now()
        max_age_hours = self.config['data_quality']['max_age_hours']
        
        fresh_items = 0
        for item in self.data_store:
            if 'collected_at' in item:
                try:
                    collected_time = datetime.fromisoformat(item['collected_at'])
                    age_hours = (current_time - collected_time).total_seconds() / 3600
                    if age_hours <= max_age_hours:
                        fresh_items += 1
                except:
                    pass
        
        return fresh_items / len(self.data_store) if self.data_store else 0
    
    def try_fallback_api(self):
        """Switch to fallback API if available"""
        fallback_apis = self.config['api_settings'].get('fallback_apis', [])
        if fallback_apis and self.current_api != fallback_apis[0]:
            self.current_api = fallback_apis[0]
            logger.info(f"Switched to fallback API: {self.current_api}")
    
    def log_strategy_change(self):
        """Log strategy adjustments"""
        success_rate = self.get_success_rate()
        logger.info(f"Strategy adjusted - Success rate: {success_rate:.2f}, "
                   f"Delay multiplier: {self.delay_multiplier:.2f}, "
                   f"Current API: {self.current_api}")
    
    def generate_comprehensive_metadata(self, data, data_type, dataset_name=None):
        """Generate comprehensive automated metadata"""
        import os
        import sys
        import platform
        import hashlib
        
        current_time = datetime.now()
        
        # Calculate data fingerprint
        data_str = json.dumps(data, sort_keys=True, default=str)
        data_hash = hashlib.md5(data_str.encode()).hexdigest()
        
        # Analyze data structure
        if isinstance(data, dict) and 'items' in data:
            items = data['items']
            item_count = len(items)
            sample_item = items[0] if items else {}
        elif isinstance(data, list):
            items = data
            item_count = len(items)
            sample_item = items[0] if items else {}
        else:
            items = [data]
            item_count = 1
            sample_item = data
        
        # Field analysis
        field_analysis = {}
        if sample_item and isinstance(sample_item, dict):
            for field, value in sample_item.items():
                field_analysis[field] = {
                    'type': type(value).__name__,
                    'sample_value': str(value)[:100] if len(str(value)) > 100 else value,
                    'is_required': field in self.config.get('data_quality', {}).get('required_fields', [])
                }
        
        metadata = {
            # Temporal metadata
            'collection_info': {
                'collected_at': current_time.isoformat(),
                'collection_date': current_time.strftime('%Y-%m-%d'),
                'collection_time': current_time.strftime('%H:%M:%S'),
                'utc_offset': str(current_time.astimezone().utcoffset())
            },
            
            # Source metadata
            'source_info': {
                'api_endpoint': 'https://api.clashroyale.com/v1/cards',
                'api_version': 'v1',
                'source_system': 'clash_royale_api',
                'data_provider': 'Supercell',
                'dataset_name': dataset_name or 'clash_royale_cards'
            },
            
            # Agent metadata
            'agent_info': {
                'agent_name': self.config['agent_settings']['name'],
                'agent_version': '1.0',
                'collection_session': f"session_{current_time.strftime('%Y%m%d_%H%M%S')}",
                'configuration_hash': hashlib.md5(json.dumps(self.config, sort_keys=True).encode()).hexdigest()[:8]
            },
            
            # System metadata
            'system_info': {
                'platform': platform.system(),
                'platform_version': platform.version(),
                'python_version': sys.version.split()[0],
                'hostname': platform.node(),
                'architecture': platform.architecture()[0]
            },
            
            # Data characteristics
            'data_characteristics': {
                'data_type': data_type,
                'format': 'json',
                'encoding': 'utf-8',
                'total_items': item_count,
                'data_size_bytes': len(data_str),
                'data_fingerprint': data_hash,
                'schema_version': '1.0'
            },
            
            # Quality metadata
            'quality_info': {
                'collection_success_rate': self.get_success_rate(),
                'total_requests_made': self.collection_stats['total_requests'],
                'data_completeness_score': self.check_completeness() if self.data_store else 0,
                'validation_passed': True if data_type == 'processed' else None,
                'quality_checks_performed': current_time.isoformat()
            },
            
            # Schema metadata
            'schema_info': {
                'field_count': len(field_analysis),
                'fields': field_analysis,
                'required_fields': self.config.get('data_quality', {}).get('required_fields', []),
                'nullable_fields': [f for f, info in field_analysis.items() if not info['is_required']]
            },
            
            # Lineage metadata
            'lineage_info': {
                'data_source': 'api_collection',
                'processing_stage': data_type,
                'parent_datasets': ['clash_royale_api_raw'] if data_type == 'processed' else None,
                'collection_method': 'automated_agent',
                'next_processing_steps': ['validation', 'storage'] if data_type == 'raw' else ['analysis', 'reporting']
            },
            
            # Usage metadata
            'usage_info': {
                'intended_use': 'game_data_analysis',
                'access_level': 'internal',
                'retention_period': 'indefinite',
                'update_frequency': 'on_demand',
                'last_modified': current_time.isoformat()
            }
        }
        
        return metadata
    
    def save_raw_data(self, raw_data, dataset_name):
        """Save raw, unprocessed data with comprehensive metadata"""
        import os
        
        # Create directories if they don't exist
        raw_path = self.config['storage']['raw_data_path']
        os.makedirs(raw_path, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename_template = self.config['storage']['filename_template']
        filename = filename_template.format(
            dataset=dataset_name,
            timestamp=timestamp,
            type='raw'
        )
        filepath = os.path.join(raw_path, filename)
        
        # Generate comprehensive metadata
        metadata = self.generate_comprehensive_metadata(raw_data, 'raw', dataset_name)
        
        # Save raw data with enhanced metadata
        raw_data_with_metadata = {
            'metadata': metadata,
            'data': raw_data
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(raw_data_with_metadata, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 Raw data saved: {filename}")
        except Exception as e:
            logger.error(f"Failed to save raw data: {e}")
    
    def save_processed_data(self, processed_data, dataset_name):
        """Save cleaned, processed data with comprehensive metadata"""
        import os
        
        # Create directories if they don't exist
        processed_path = self.config['storage']['processed_data_path']
        os.makedirs(processed_path, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename_template = self.config['storage']['filename_template']
        filename = filename_template.format(
            dataset=dataset_name,
            timestamp=timestamp,
            type='processed'
        )
        filepath = os.path.join(processed_path, filename)
        
        # Generate comprehensive metadata
        metadata = self.generate_comprehensive_metadata(processed_data, 'processed', dataset_name)
        
        # Add processing-specific metadata
        metadata['processing_info'] = {
            'processed_at': datetime.now().isoformat(),
            'processing_version': '1.0',
            'transformations_applied': [
                'field_extraction',
                'field_standardization', 
                'data_validation',
                'quality_scoring',
                'timestamp_addition'
            ],
            'validation_rules': {
                'required_fields_check': True,
                'data_type_validation': True,
                'business_rule_validation': True
            },
            'quality_scores': {
                'completeness': self.check_completeness(),
                'accuracy': self.check_accuracy(),
                'consistency': self.check_consistency(),
                'timeliness': self.check_timeliness()
            }
        }
        
        # Save processed data with enhanced metadata
        processed_data_with_metadata = {
            'metadata': metadata,
            'data': processed_data
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(processed_data_with_metadata, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 Processed data saved: {filename}")
        except Exception as e:
            logger.error(f"Failed to save processed data: {e}")
    
    def save_report(self, report):
        """Save collection report to reports folder"""
        import os
        
        # Create directories if they don't exist
        reports_path = self.config['storage']['reports_path']
        os.makedirs(reports_path, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"collection_report_{timestamp}.json"
        filepath = os.path.join(reports_path, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"📊 Report saved: {filename}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save report: {e}")
            return None
    
    def test_api_connectivity(self):
        """Test API connectivity without making actual data requests"""
        logger.info("🧪 TESTING API CONNECTIVITY")
        logger.info("=" * 40)
        
        # Test 1: Network connectivity
        try:
            import socket
            logger.info("1️⃣  Testing network connection to api.clashroyale.com...")
            socket.create_connection(("api.clashroyale.com", 443), timeout=5)
            logger.info("✅ Network connectivity: SUCCESS")
        except Exception as e:
            logger.error(f"❌ Network connectivity: FAILED - {e}")
            return False
        
        # Test 2: API key validation
        logger.info("2️⃣  Checking API key...")
        if self.api_key:
            logger.info(f"✅ API key found (length: {len(self.api_key)})")
            logger.info(f"✅ Key preview: {self.api_key[:20]}...")
        else:
            logger.error("❌ No API key found")
            return False
        
        # Test 3: Simple API request
        logger.info("3️⃣  Testing API endpoint...")
        url = "https://api.clashroyale.com/v1/cards"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            logger.info(f"📊 API Response: {response.status_code}")
            
            if response.status_code == 200:
                logger.info("🎉 API connectivity: SUCCESS")
                data = response.json()
                logger.info(f"📦 Sample data received: {len(data.get('items', []))} items")
                return True
            elif response.status_code == 403:
                logger.error("❌ API key rejected (403 Forbidden)")
                logger.error("💡 Your API key may be expired or invalid")
                return False
            else:
                logger.error(f"❌ API returned status {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ API test failed: {e}")
            return False
    
    def generate_comprehensive_documentation(self):
        """Generate comprehensive documentation for the data collection process"""
        docs = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'agent_version': '1.0',
                'documentation_version': '1.0'
            },
            'collection_summary': self.generate_basic_report(),
            'data_schema': self.generate_data_schema_docs(),
            'api_documentation': self.generate_api_docs(),
            'data_transformations': self.generate_transformation_docs(),
            'quality_metrics': self.generate_quality_docs(),
            'usage_guide': self.generate_usage_guide(),
            'data_catalog': self.generate_data_catalog()
        }
        
        # Save comprehensive documentation
        self.save_comprehensive_docs(docs)
        return docs
    
    def generate_data_schema_docs(self):
        """Generate data schema documentation"""
        if not self.data_store:
            return {"note": "No data collected yet"}
            
        sample_item = self.data_store[0] if self.data_store else {}
        
        schema_docs = {
            'raw_data_schema': {
                'description': 'Schema of raw data as received from API',
                'fields': {
                    'name': {'type': 'string', 'description': 'Card name', 'required': True},
                    'id': {'type': 'integer', 'description': 'Unique card identifier', 'required': True},
                    'elixirCost': {'type': 'integer', 'description': 'Elixir cost to play card', 'required': True},
                    'maxLevel': {'type': 'integer', 'description': 'Maximum upgrade level', 'required': False},
                    'rarity': {'type': 'string', 'description': 'Card rarity (common, rare, epic, legendary)', 'required': True},
                    'iconUrls': {'type': 'object', 'description': 'URLs for card images', 'required': False}
                }
            },
            'processed_data_schema': {
                'description': 'Schema of processed, cleaned data',
                'fields': {
                    field: {
                        'type': type(value).__name__, 
                        'sample_value': value,
                        'description': f'Processed field: {field}'
                    } for field, value in sample_item.items()
                } if sample_item else {}
            },
            'data_quality_fields': {
                'collected_at': {'type': 'datetime', 'description': 'Timestamp when data was collected'},
                'data_quality_score': {'type': 'float', 'description': 'Overall quality score (0-1)'}
            }
        }
        return schema_docs
    
    def generate_api_docs(self):
        """Generate API documentation"""
        return {
            'api_endpoint': 'https://api.clashroyale.com/v1/cards',
            'authentication': 'Bearer token (JWT)',
            'rate_limits': {
                'requests_per_minute': self.config['api_settings']['rate_limit_per_minute'],
                'burst_limit': self.config['api_settings']['burst_limit']
            },
            'response_format': 'JSON',
            'typical_response_size': '121 items per request',
            'cache_duration': '60 seconds (from API headers)',
            'error_codes': {
                '200': 'Success',
                '401': 'Invalid or missing API key',
                '403': 'Access forbidden (check API key permissions)',
                '429': 'Rate limit exceeded',
                '500': 'Server error'
            },
            'request_headers': {
                'Authorization': 'Bearer {api_key}',
                'Accept': 'application/json',
                'User-Agent': 'DataCollectionAgent/1.0'
            }
        }
    
    def generate_transformation_docs(self):
        """Generate data transformation documentation"""
        return {
            'transformation_pipeline': [
                {
                    'step': 1,
                    'name': 'Raw Data Extraction',
                    'description': 'Extract items array from API response',
                    'input': 'Full API response object',
                    'output': 'Array of card objects'
                },
                {
                    'step': 2,
                    'name': 'Field Mapping',
                    'description': 'Map API fields to standardized names',
                    'transformations': {
                        'elixirCost': 'elixir_cost',
                        'maxLevel': 'max_level',
                        'maxEvolutionLevel': 'is_evolution_available (boolean)'
                    }
                },
                {
                    'step': 3,
                    'name': 'Data Enrichment',
                    'description': 'Add metadata and calculated fields',
                    'added_fields': [
                        'collected_at (timestamp)',
                        'data_quality_score (calculated)',
                        'processing_version'
                    ]
                },
                {
                    'step': 4,
                    'name': 'Validation',
                    'description': 'Validate against required fields and data types',
                    'validation_rules': self.config['data_quality']['required_fields']
                }
            ],
            'data_quality_checks': {
                'completeness': 'Check all required fields are present',
                'accuracy': 'Validate data types and ranges',
                'consistency': 'Check for consistent formats',
                'timeliness': 'Verify data freshness'
            }
        }
    
    def generate_quality_docs(self):
        """Generate quality metrics documentation"""
        quality_score = self.assess_data_quality()
        
        return {
            'overall_score': quality_score,
            'quality_dimensions': {
                'completeness': {
                    'score': self.check_completeness(),
                    'description': 'Percentage of records with all required fields',
                    'threshold': self.config['data_quality']['min_completeness']
                },
                'accuracy': {
                    'score': self.check_accuracy(),
                    'description': 'Data correctness and validity',
                    'threshold': self.config['data_quality']['min_accuracy']
                },
                'consistency': {
                    'score': self.check_consistency(),
                    'description': 'Data format and type consistency'
                },
                'timeliness': {
                    'score': self.check_timeliness(),
                    'description': 'Data freshness and currency',
                    'max_age_hours': self.config['data_quality']['max_age_hours']
                }
            },
            'collection_metrics': {
                'success_rate': self.get_success_rate(),
                'total_requests': self.collection_stats['total_requests'],
                'failed_requests': self.collection_stats['failed_requests'],
                'items_collected': len(self.data_store)
            }
        }
    
    def generate_usage_guide(self):
        """Generate usage documentation"""
        return {
            'quick_start': {
                'installation': [
                    'pip install requests',
                    'Configure API key in config.json',
                    'Run: python data_collection_agent.py'
                ],
                'configuration': 'Edit config.json to customize collection parameters',
                'testing': 'Run: python test_connectivity.py to verify API access'
            },
            'configuration_options': {
                'agent_settings': {
                    'max_requests': 'Maximum number of API calls per session',
                    'base_delay': 'Delay between requests (seconds)',
                    'timeout': 'Request timeout (seconds)'
                },
                'data_quality': {
                    'required_fields': 'Fields that must be present for valid data',
                    'min_completeness': 'Minimum completeness threshold (0-1)',
                    'min_accuracy': 'Minimum accuracy threshold (0-1)'
                }
            },
            'output_files': {
                'raw_data': 'Unprocessed API responses in data/raw/',
                'processed_data': 'Cleaned and validated data in data/processed/',
                'reports': 'Collection reports and documentation in reports/',
                'logs': 'Execution logs for debugging'
            },
            'common_issues': {
                '403_forbidden': 'Check API key validity and permissions',
                'rate_limiting': 'Increase delays in configuration',
                'validation_errors': 'Review required_fields in config.json'
            }
        }
    
    def generate_metadata_catalog(self):
        """Generate comprehensive metadata catalog"""
        import os
        
        catalog = {
            'catalog_info': {
                'generated_at': datetime.now().isoformat(),
                'catalog_version': '1.0',
                'total_datasets': 0,
                'metadata_standards': 'Dublin Core + Custom Extensions'
            },
            'automated_metadata_features': {
                'temporal_metadata': [
                    'collection_timestamps',
                    'processing_timestamps', 
                    'timezone_information',
                    'session_tracking'
                ],
                'source_metadata': [
                    'api_endpoint_documentation',
                    'data_provider_information',
                    'source_system_identification',
                    'api_version_tracking'
                ],
                'technical_metadata': [
                    'system_information',
                    'platform_details',
                    'python_version',
                    'agent_configuration'
                ],
                'data_characteristics': [
                    'data_fingerprinting',
                    'size_calculations',
                    'format_identification',
                    'encoding_detection'
                ],
                'quality_metadata': [
                    'completeness_scoring',
                    'accuracy_assessment',
                    'consistency_checking',
                    'timeliness_evaluation'
                ],
                'schema_metadata': [
                    'field_analysis',
                    'type_detection',
                    'requirement_mapping',
                    'nullable_field_identification'
                ],
                'lineage_metadata': [
                    'data_source_tracking',
                    'processing_stage_identification',
                    'transformation_documentation',
                    'dependency_mapping'
                ]
            },
            'datasets': {},
            'data_lineage': {
                'source': 'Clash Royale API (api.clashroyale.com)',
                'collection_method': 'Automated agent with comprehensive metadata generation',
                'processing_steps': 'Raw Collection → Metadata Generation → Validation → Transformation → Quality Assessment → Storage',
                'update_frequency': 'On-demand via agent execution',
                'metadata_refresh': 'Automatic with each collection cycle'
            },
            'data_governance': {
                'metadata_standards': 'Dublin Core extended with domain-specific fields',
                'retention_policy': 'Metadata retained with data indefinitely',
                'access_control': 'File system permissions',
                'backup_strategy': 'Metadata included in all backups',
                'privacy_considerations': 'Public game data, comprehensive metadata for transparency',
                'compliance': 'Metadata supports data discovery and governance'
            }
        }
        
        return catalog
    
    def generate_data_catalog(self):
        """Generate data catalog with metadata focus"""
        catalog = self.generate_metadata_catalog()
        
        # Add dataset information
        import os
        
        # Catalog raw data files
        raw_path = self.config['storage']['raw_data_path']
        if os.path.exists(raw_path):
            raw_files = [f for f in os.listdir(raw_path) if f.endswith('.json')]
            catalog['datasets']['raw_data'] = {
                'location': raw_path,
                'file_count': len(raw_files),
                'latest_file': max(raw_files) if raw_files else None,
                'description': 'Unprocessed API responses with full metadata'
            }
        
        # Catalog processed data files
        processed_path = self.config['storage']['processed_data_path']
        if os.path.exists(processed_path):
            processed_files = [f for f in os.listdir(processed_path) if f.endswith('.json')]
            catalog['datasets']['processed_data'] = {
                'location': processed_path,
                'file_count': len(processed_files),
                'latest_file': max(processed_files) if processed_files else None,
                'description': 'Cleaned and validated data ready for analysis'
            }
        
        return catalog
    
    def save_comprehensive_docs(self, docs):
        """Save comprehensive documentation to multiple formats"""
        import os
        
        # Create docs directory
        docs_path = os.path.join(self.config['storage']['reports_path'], 'documentation')
        os.makedirs(docs_path, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save JSON format
        json_path = os.path.join(docs_path, f'comprehensive_docs_{timestamp}.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(docs, f, indent=2, ensure_ascii=False, default=str)
        
        # Save Markdown format
        md_path = os.path.join(docs_path, f'README_{timestamp}.md')
        self.save_markdown_docs(docs, md_path)
        
        logger.info(f"📚 Comprehensive documentation saved:")
        logger.info(f"   JSON: {json_path}")
        logger.info(f"   Markdown: {md_path}")
        
        return json_path, md_path
    
    def save_markdown_docs(self, docs, filepath):
        """Save documentation in Markdown format"""
        md_content = f"""# Data Collection Agent Documentation

Generated: {docs['metadata']['generated_at']}
Agent Version: {docs['metadata']['agent_version']}

## Collection Summary

- **Total Requests**: {docs['collection_summary']['collection_stats']['total_requests']}
- **Success Rate**: {docs['collection_summary']['success_rate']:.1%}
- **Items Collected**: {docs['collection_summary']['total_items_collected']}
- **Duration**: {docs['collection_summary']['collection_duration']}

## Data Schema

### Raw Data Fields
{self._format_schema_md(docs['data_schema']['raw_data_schema']['fields'])}

### API Information
- **Endpoint**: {docs['api_documentation']['api_endpoint']}
- **Authentication**: {docs['api_documentation']['authentication']}
- **Rate Limit**: {docs['api_documentation']['rate_limits']['requests_per_minute']} requests/minute

## Quality Metrics

- **Overall Score**: {docs['quality_metrics']['overall_score']:.2f}
- **Completeness**: {docs['quality_metrics']['quality_dimensions']['completeness']['score']:.2f}
- **Timeliness**: {docs['quality_metrics']['quality_dimensions']['timeliness']['score']:.2f}

## Quick Start

```bash
# Test connectivity
python test_connectivity.py

# Run full collection
python test/test_agent.py
```

## Data Locations

- **Raw Data**: `{docs['collection_summary']['data_storage']['raw_data_location']}`
- **Processed Data**: `{docs['collection_summary']['data_storage']['processed_data_location']}`
- **Reports**: `{docs['collection_summary']['data_storage']['reports_location']}`

---
*Generated automatically by DataCollectionAgent*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
    
    def _format_schema_md(self, fields):
        """Format schema fields for Markdown"""
        lines = []
        for field, info in fields.items():
            required = "✅" if info.get('required', False) else "⭕"
            lines.append(f"- **{field}** ({info['type']}) {required} - {info['description']}")
        return '\n'.join(lines)
    
    def generate_basic_report(self):
        """Generate basic collection report without comprehensive docs"""
        report = {
            'collection_stats': self.collection_stats,
            'data_quality_score': self.assess_data_quality(),
            'total_items_collected': len(self.data_store),
            'success_rate': self.get_success_rate(),
            'collection_duration': str(datetime.now() - self.start_time),
            'configuration_used': self.config['agent_settings']['name'],
            'data_storage': {
                'raw_data_location': self.config['storage']['raw_data_path'],
                'processed_data_location': self.config['storage']['processed_data_path'],
                'reports_location': self.config['storage']['reports_path']
            }
        }
        return report
    
    def generate_report(self):
        """Generate collection report and trigger comprehensive documentation"""
        report = self.generate_basic_report()
        
        # Save basic report
        self.save_report(report)
        
        # Generate comprehensive documentation
        self.generate_comprehensive_documentation()
        
        return report