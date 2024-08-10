from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os, requests, json, pandas as pd, time, sshtunnel, logging, MySQLdb, numpy as np
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from paramiko.ssh_exception import AuthenticationException

app = Flask(__name__)
app.secret_key = os.urandom(30)
pythonserverpass = os.environ.get('serverkey')

def get_sql_key():
    return sql_key

sql_key = get_sql_key()
engine_url = f'mysql://tomasdevelopment:{sql_key}@tomasdevelopment.mysql.heroku-services.com/tomasdevelopment$tokens_db'
engine2 = create_engine(engine_url)

global_access_token = None

@app.route('/')
def home():
    return "Flask app is running"

def fetch_token_data(company_name):
    try:
        with sshtunnel.SSHTunnelForwarder(
            ('ssh.heroku.com', 22),
            ssh_username='tomasdevelopment', ssh_password='passtest123!',
            remote_bind_address=('tomasdevelopment.mysql.heroku-services.com', 3306)
        ) as tunnel:
            connection = MySQLdb.connect(
                user='tomasdevelopment', passwd=sql_key,
                host='127.0.0.1', port=tunnel.local_bind_port,
                db='tomasdevelopment$tokenz',
            )
            query = "SELECT * FROM accholder_tiktok_token WHERE Company_Name = %s"
            df = pd.read_sql(query, connection, params=[company_name])
            connection.close()

        if not df.empty:
            result = df.iloc[0].to_dict()
            for key, value in result.items():
                if isinstance(value, np.int64):
                    result[key] = int(value)
                elif isinstance(value, datetime):
                    result[key] = value.strftime('%Y-%m-%d %H:%M:%S')
            return result
        return None
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return None

def refresh_access_token(refresh_token):
    url = 'https://open.tiktokapis.com/v2/oauth/token/'
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "client_key": app_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    response = requests.post(url, headers=headers, data=body)
    return response.json() if response.status_code == 200 else None

def update_access_token(company_name, new_access_token, expires_in):
    try:
        with sshtunnel.SSHTunnelForwarder(
            ('ssh.heroku.com', 22),
            ssh_username='tomasdevelopment', ssh_password='testpass123',
            remote_bind_address=('tomasdevelopment.mysql.heroku-services.com', 3306)
        ) as tunnel:
            connection = MySQLdb.connect(
                user='tomasdevelopment', passwd='123',
                host='127.0.0.1', port=tunnel.local_bind_port,
                db='tomasdevelopment$tokenz',
            )
            with connection.cursor() as cursor:
                query = """
                        UPDATE accholder_tiktok_token
                        SET access_token = %s, expires_in = %s, date_of_update = NOW()
                        WHERE company_name = %s
                        """
                cursor.execute(query, (new_access_token, expires_in, company_name))
                connection.commit()
    except Exception as e:
        logging.error(f"An error occurred while updating the access token: {str(e)}")

@app.route('/refresh-tiktok-token', methods=['POST'])
def handle_token_refresh():
    auth_token = request.headers.get('Authorization')
    if auth_token != secret_token:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    company_name = data.get('company_name')
    if not company_name:
        return jsonify({'error': 'Missing data'}), 400

    token_data = fetch_token_data(company_name)
    if not token_data:
        return jsonify({'error': 'Company not found or unable to fetch current token data'}), 404

    refresh_token = token_data.get('refresh_token')
    expires_in = token_data.get('expires_in', 0)
    date_of_update = datetime.strptime(token_data.get('date_of_update', ''), '%Y-%m-%d %H:%M:%S')
    hours_passed = (datetime.now() - date_of_update).total_seconds() / 3600
    hours_left = (expires_in / 3600) - hours_passed

    if hours_left <= 1:
        refresh_response = refresh_access_token(refresh_token)
        if 'access_token' in refresh_response:
            new_access_token = refresh_response.get('access_token')
            new_expires_in = refresh_response.get('expires_in')
            update_access_token(company_name, new_access_token, new_expires_in)
            return jsonify({'message': f'Access token refreshed successfully with hours left access {hours_left}', 'access_token': new_access_token}), 200
        return jsonify({'error': 'Failed to refresh the access token'}), 500
    return jsonify({'message': f'Current token is still valid, no need to refresh', 'access_token': token_data.get('access_token')}), 200

@app.route('/TiktokAccData', methods=['POST'])
def pulltokensdataaccholder():
    received_token = request.headers.get('Authorization', None)
    if received_token != secret_token:
        return jsonify({'error': 'Invalid or missing token'}), 401

    company_name = request.json.get('company_name')
    if not company_name:
        return jsonify({'error': 'Missing required data'}), 400

    token_data = fetch_token_data(company_name)
    return jsonify(token_data) if token_data else (jsonify({'error': 'Company not found'}), 404)

@app.route('/TiktokAdvData', methods=['GET'])
def pulltokensdataadvertiser():
    received_token = request.headers.get('Authorization', None)
    if received_token != secret_token:
        return jsonify({'error': 'Invalid or missing token'}), 401

    data = request.json
    company_name = data.get('company_name')
    acchldr_url = data.get('acchldr_url', '')

    if not company_name or not acchldr_url:
        return jsonify({'error': 'Missing required data'}), 400

    try:
        with sshtunnel.SSHTunnelForwarder(
            ('ssh.heroku.com', 22),
            ssh_username='tomasdevelopment', ssh_password='testpasswors123!',
            remote_bind_address=('tomasdevelopment.mysql.heroku-services.com', 3306)
        ) as tunnel:
            connection = MySQLdb.connect(
                user='tomasdevelopment', passwd='Io5EdhmO2bhybudT',
                host='127.0.0.1', port=tunnel.local_bind_port,
                db='tomasdevelopment$tokenz',
            )
            query = "SELECT * FROM adv_tiktok_token WHERE Company_Name = %s"
            df = pd.read_sql(query, connection, params=[company_name])
            connection.close()

            if not df.empty:
                return jsonify({'access_token': df.iloc[0]['access_token']})
            return jsonify({'error': 'Company not found'}), 404
    except AuthenticationException:
        return jsonify({'error': 'Authentication failed. Please check your credentials.'}), 401
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

def build_url(path, query=""):
    scheme, netloc = "https", "business-api.tiktok.com"
    return urlunparse((scheme, netloc, path, "", query, ""))

def fetch_tiktok_token(auth_code, company_name):
    try:
        secret = client_secret
        my_args = json.dumps({
            "secret": secret,
            "app_id": app_id,
            "auth_code": auth_code
        })
        PATH = "/open_api/v1.3/oauth2/access_token/"
        url = build_url(PATH)
        args = json.loads(my_args)
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, json=args)

        if response.status_code == 200:
            data = response.json().get('data', {})
            if 'advertiser_ids' in data and isinstance(data['advertiser_ids'], list):
                data['advertiser_ids'] = json.dumps(data['advertiser_ids'])
            data.pop('scope', None)
            return {'status': 'success', 'data': data}
        return {'status': 'error', 'message': f'Failed to get access token: {response.text}'}
    except Exception as e:
        return {'status': 'error', 'message': f'An exception occurred: {e}'}

def remove_duplicates(engine, table_name):
    with engine.begin() as conn:
        remove_dup_query = f"""
        DELETE t1 FROM {table_name} t1
        INNER JOIN (
            SELECT Company_Name, MAX(date_of_update) as latest_date
            FROM {table_name}
            WHERE Company_Name IS NOT NULL AND Company_Name != ''
            GROUP BY Company_Name
            HAVING COUNT(*) > 1
        ) t2 ON t1.Company_Name = t2.Company_Name
        WHERE t1.date_of_update < t2.latest_date;
        """
        result = conn.execute(text(remove_dup_query))
    return result.rowcount

def extract_codes_from_url(acchldr_url, advertiser_url):
    codes = {'accholder': None, 'advertiser': None}
    parsed_url = urlparse(acchldr_url)
    query_params = parse_qs(parsed_url.query)
    codes['accholder'] = query_params.get('code', [None])[0]

    if advertiser_url:
        parsed_url = urlparse(advertiser_url)
        query_params = parse_qs(parsed_url.query)
        codes['advertiser'] = query_params.get('auth_code', [None])[0]
    return codes

def get_access_tokens(codes, company_name):
    account_holder_tokens = []
    advertiser_tokens = []

    if codes['accholder']:
        auth_code = codes['accholder']
        url = 'https://open.tiktokapis.com/v2/oauth/token/'
        body = {
            "client_key": app_id,
            "client_secret": client_secret,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url, headers=headers, data=urlencode(body))
        if response.status_code == 200:
            json_response = response.json()
            json_response['user_type'] = 'accholder'
            account_holder_tokens.append(json_response)
        else:
            logging.error(f"Error fetching account holder token: {response.text}")

    if codes['advertiser']:
        result = fetch_tiktok_token(codes['advertiser'], company_name)
        if result['status'] == 'success':
            data = result['data']
            data['user_type'] = 'advertiser'
            advertiser_tokens.append(data)
        else:
            logging.error(f"Error fetching advertiser token: {result['message']}")

    account_holder_df = pd.DataFrame(account_holder_tokens)
    advertiser_df = pd.DataFrame(advertiser_tokens)

    account_holder_df["Company_Name"] = company_name
    account_holder_df["date_of_update"] = datetime.utcnow()
    advertiser_df["Company_Name"] = company_name
    advertiser_df["date_of_update"] = datetime.utcnow()

    if not account_holder_df.empty:
        account_holder_df.to_sql('accholder_tiktok_token', con=engine2, if_exists='append', index=False)
        remove_duplicates(engine2, 'accholder_tiktok_token')
    if not advertiser_df.empty:
        advertiser_df.to_sql('adv_tiktok_token', con=engine2, if_exists='append', index=False)
        remove_duplicates(engine2, 'adv_tiktok_token')

    return account_holder_df, advertiser_df

@app.route('/authenticate_all_tiktok', methods=['POST'])
def authenticate():
    received_token = request.headers.get('Authorization', None)
    if received_token != secret_token:
        return jsonify({'error': 'Invalid or missing token'}), 401

    data = request.json
    company_name = data.get('company_name')
    acchldr_url = data.get('acchldr_url', '')
    advertiser_url = data.get('advertiser_url', '')

    if not company_name or not acchldr_url:
        return jsonify({'error': 'Missing required parameters: company_name and/or acchldr_url'}), 400

    codes = extract_codes_from_url(acchldr_url, advertiser_url)
    account_holder_df, advertiser_df = get_access_tokens(codes, company_name)

    response_data = {
        'account_holder_tokens': account_holder_df.to_dict(orient='records'),
        'advertiser_tokens': advertiser_df.to_dict(orient='records')
    }
    return jsonify({'message': 'Tokens fetched and saved successfully', 'data': response_data})

def manage_access_token(company_name):
    token_data = fetch_token_data(company_name)
    return token_data.get('access_token') if token_data else None

def manage_open_id(company_name):
    token_data = fetch_token_data(company_name)
    return token_data.get('open_id') if token_data else None
def refresh_tiktok_token_direct(company_name):
    token_data = fetch_token_data(company_name)
    if not token_data:
        return {'error': 'Company not found or unable to fetch current token data'}, 404

    refresh_token = token_data.get('refresh_token')
    expires_in = token_data.get('expires_in', 0)
    date_of_update_str = token_data.get('date_of_update', '')

    date_of_update = datetime.strptime(date_of_update_str, '%Y-%m-%d %H:%M:%S')
    hours_passed = (datetime.now() - date_of_update).total_seconds() / 3600
    hours_left = (expires_in / 3600) - hours_passed

    if hours_left <= 2:
        refresh_response = refresh_access_token(refresh_token)
        if 'access_token' in refresh_response:
            new_access_token = refresh_response['access_token']
            new_expires_in = refresh_response['expires_in']
            update_access_token(company_name, new_access_token, new_expires_in)
            return {'access_token': new_access_token}, 200
        else:
            return {'error': 'Failed to refresh access token'}, 500
    else:
        return {'access_token': token_data['access_token']}, 200

@app.route('/get_tiktok_data', methods=['POST'])
def get_tiktok_data():
    received_token = request.headers.get('Authorization', None)
    if received_token != secret_token:
        return jsonify({'error': 'Invalid or missing token'}), 401

    company_name = request.json.get('company_name')
    if not company_name:
        return jsonify({'error': 'Missing company_name'}), 400

    token_refresh_result, status_code = refresh_tiktok_token_direct(company_name)
    if 'error' in token_refresh_result:
        return jsonify({'error': token_refresh_result['error']}), status_code

    global_access_token = token_refresh_result['access_token']
    open_id = manage_open_id(company_name)

    if not global_access_token:
        return jsonify({'error': 'Failed to obtain access token'}), 401

    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=59)
    profile_url = 'https://business-api.tiktok.com/open_api/v1.3/business/get/'

    headers = {'Access-Token': global_access_token}
    params = {
        'business_id': open_id,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'fields': json.dumps(['username', 'followers_count', 'audience_genders',
                              'audience_countries', 'profile_image', 'profile_views',
                              'is_business_account', 'video_views', 'comments', 'likes',
                              'shares', 'audience_activity', 'display_name'])
    }
    response = requests.get(profile_url, headers=headers, params=params)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Failed to retrieve detailed data', 'details': response.text}), 400

@app.route('/get_tiktok_data_organic', methods=['POST'])
def get_tiktok_data_organic():
    received_token = request.headers.get('Authorization', None)
    if received_token != secret_token:
        return jsonify({'error': 'Invalid or missing token'}), 401

    company_name = request.json.get('company_name')
    if not company_name:
        return jsonify({'error': 'Missing company_name'}), 400

    token_refresh_result, _ = refresh_tiktok_token_direct(company_name)
    global_access_token = token_refresh_result['access_token']
    profile_url = 'https://open.tiktokapis.com/v2/user/info/'

    if not global_access_token:
        return jsonify({'error': 'Failed to obtain access token'}), 401

    fields = 'username,follower_count,following_count,likes_count,video_count,open_id'
    params = {'fields': fields}
    headers = {
        'Authorization': f'Bearer {global_access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(profile_url, headers=headers, params=params)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Failed to retrieve simplified data', 'details': response.text}), 400

@app.route('/get_tiktok_data_organic_video', methods=['POST'])
def get_tiktok_data_organic_video():
    received_token = request.headers.get('Authorization', None)
    if received_token != secret_token:
        return jsonify({'error': 'Invalid or missing token'}), 401

    company_name = request.json.get('company_name')
    if not company_name:
        return jsonify({'error': 'Missing company_name'}), 400

    open_id = manage_open_id(company_name)
    token_refresh_result, status_code = refresh_tiktok_token_direct(company_name)
    if 'error' in token_refresh_result:
        return jsonify({'error': token_refresh_result['error']}), status_code

    global_access_token = token_refresh_result['access_token']
    app.logger.debug(f"Using access token: {global_access_token}")

    if not global_access_token:
        app.logger.error(f"Failed to obtain access token for company: {company_name}")
        return jsonify({'error': 'Failed to obtain access token'}), 401

    profile_url = 'https://business-api.tiktok.com/open_api/v1.3/business/video/list/'
    headers = {'Access-Token': global_access_token}
    params = {
        'business_id': open_id,
        'fields': json.dumps([
            "item_id", "create_time", "thumbnail_url", "share_url", "caption",
            "video_views", "likes", "comments", "shares", "reach", "video_duration",
            "full_video_watched_rate", "total_time_watched", "average_time_watched",
            "impression_sources", "audience_countries"
        ])
    }

    response = requests.get(profile_url, headers=headers, params=params)
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({
            'error': 'Failed to retrieve data',
            'details': response.text
        }), response.status_code

# Global variables for rate limiting
call_count = 0
start_time = datetime.now()

# Rate limit configuration
base_calls_per_hour = 300
additional_calls_per_ad = 40

def check_rate_limit():
    global call_count, start_time
    current_time = datetime.now()
    elapsed_time = current_time - start_time

    if elapsed_time >= timedelta(hours=1):
        call_count = 0
        start_time = current_time

    if call_count >= (base_calls_per_hour + additional_calls_per_ad * get_active_ads_count()):
        return False
    return True

def get_active_ads_count():
    return 10  # Example value, replace with your logic to fetch the count of active ads

if __name__ == '__main__':
    app.run(debug=True)
