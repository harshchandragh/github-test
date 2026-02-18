import requests
import sys
from datetime import datetime
import os

class JiraAnalyticsAPITester:
    def __init__(self, base_url="https://jira-velocity-pro.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.upload_result = None

    def run_test(self, name, method, endpoint, expected_status, data=None, files=None):
        """Run a single API test"""
        url = f"{self.api_base}/{endpoint}"
        headers = {'Content-Type': 'application/json'} if not files else {}
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                if files:
                    response = requests.post(url, files=files, timeout=60)
                else:
                    response = requests.post(url, json=data, headers=headers, timeout=30)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ PASSED - Status: {response.status_code}")
                
                # Print response details for successful tests
                try:
                    resp_json = response.json()
                    if isinstance(resp_json, list):
                        print(f"   Response: List with {len(resp_json)} items")
                        if len(resp_json) > 0:
                            print(f"   Sample item keys: {list(resp_json[0].keys()) if resp_json[0] else 'No keys'}")
                    elif isinstance(resp_json, dict):
                        print(f"   Response keys: {list(resp_json.keys())}")
                        # Print some key values for insight
                        for key, value in list(resp_json.items())[:3]:
                            print(f"   {key}: {value}")
                except:
                    print(f"   Response: {response.text[:100]}...")
            else:
                print(f"❌ FAILED - Expected {expected_status}, got {response.status_code}")
                print(f"   Error: {response.text[:200]}")

            return success, response.json() if success else {}

        except requests.RequestException as e:
            print(f"❌ FAILED - Network Error: {str(e)}")
            return False, {}
        except Exception as e:
            print(f"❌ FAILED - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root API", "GET", "", 200)

    def test_upload_csv(self):
        """Test CSV upload with the test data"""
        print(f"\n📁 Testing CSV Upload with test data...")
        
        # Check if Raw.xlsx exists
        if not os.path.exists("/app/Raw.xlsx"):
            print("❌ Test data file /app/Raw.xlsx not found")
            return False, {}
        
        with open("/app/Raw.xlsx", 'rb') as f:
            files = {'file': ('Raw.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            success, response = self.run_test("Upload CSV/Excel", "POST", "upload-csv", 200, files=files)
            
            if success:
                self.upload_result = response
                print(f"   📊 Uploaded: {response.get('total_issues', 'N/A')} issues, {response.get('total_sprints', 'N/A')} sprints")
            
            return success, response

    def test_dashboard(self):
        """Test dashboard endpoint"""
        success, response = self.run_test("Dashboard Stats", "GET", "dashboard", 200)
        
        if success:
            print(f"   📈 Dashboard: {response.get('total_sprints', 'N/A')} sprints, {response.get('total_issues', 'N/A')} issues")
            print(f"   📊 Avg Velocity: {response.get('average_velocity', 'N/A')}, At Risk: {response.get('at_risk_sprints', 'N/A')}")
        
        return success, response

    def test_sprints(self):
        """Test sprints endpoint"""
        success, response = self.run_test("Sprints Data", "GET", "sprints", 200)
        
        if success:
            print(f"   🏃 Found {len(response)} sprints")
            if len(response) > 0:
                sample_sprint = response[0]
                print(f"   Sample Sprint: {sample_sprint.get('sprint_name', 'N/A')}")
                print(f"   Risk Level: {sample_sprint.get('risk_level', 'N/A')}, Completion: {sample_sprint.get('completion_percentage', 0):.1f}%")
        
        return success, response

    def test_recommendations(self):
        """Test recommendations endpoint"""
        success, response = self.run_test("AI Recommendations", "GET", "recommendations", 200)
        
        if success:
            print(f"   💡 Generated {len(response)} recommendations")
            if len(response) > 0:
                # Count by type
                types = {}
                for rec in response:
                    rec_type = rec.get('prompt_type', 'unknown')
                    types[rec_type] = types.get(rec_type, 0) + 1
                print(f"   Types: {types}")
                
                # Show sample AI recommendation
                ai_rec = next((r for r in response if 'AI Insight' in r.get('title', '')), None)
                if ai_rec:
                    print(f"   🤖 AI Insight: {ai_rec.get('message', '')[:100]}...")
        
        return success, response

    def test_team_performance(self):
        """Test team performance endpoint"""
        success, response = self.run_test("Team Performance", "GET", "team-performance", 200)
        
        if success:
            print(f"   👥 Found {len(response)} team members")
            if len(response) > 0:
                top_performer = response[0]
                print(f"   Top Performer: {top_performer.get('name', 'N/A')}")
                print(f"   Assigned: {top_performer.get('assigned_points', 0):.1f}, Completed: {top_performer.get('completed_points', 0):.1f}")
        
        return success, response

    def test_without_upload(self):
        """Test endpoints without data upload (should return 404)"""
        print(f"\n🚫 Testing endpoints without uploaded data (expect 404s)...")
        
        endpoints = [
            ("dashboard", "Dashboard without data"),
            ("sprints", "Sprints without data"), 
            ("recommendations", "Recommendations without data"),
            ("team-performance", "Team Performance without data")
        ]
        
        for endpoint, name in endpoints:
            success, _ = self.run_test(name, "GET", endpoint, 404)

def main():
    print("🚀 Starting Jira Analytics API Tests")
    print("=" * 50)
    
    # Setup
    tester = JiraAnalyticsAPITester()
    
    print(f"\n📡 Testing against: {tester.base_url}")
    
    # Test 1: Root endpoint
    tester.test_root_endpoint()
    
    # Test 2: Test endpoints without data (should fail)
    tester.test_without_upload()
    
    # Test 3: Upload test data
    upload_success, _ = tester.test_upload_csv()
    
    if not upload_success:
        print("\n❌ Upload failed, cannot continue with data-dependent tests")
        print(f"\n📊 Final Results: {tester.tests_passed}/{tester.tests_run} tests passed")
        return 1
    
    # Test 4: Test all endpoints with uploaded data
    print(f"\n📈 Testing endpoints with uploaded data...")
    tester.test_dashboard()
    tester.test_sprints() 
    tester.test_recommendations()
    tester.test_team_performance()
    
    # Print final results
    print("\n" + "=" * 50)
    print(f"📊 Final Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests PASSED! Backend API is working correctly.")
        return 0
    else:
        failed = tester.tests_run - tester.tests_passed
        print(f"⚠️  {failed} test(s) FAILED. Backend needs attention.")
        return 1

if __name__ == "__main__":
    sys.exit(main())