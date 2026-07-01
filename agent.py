import re
from catalog_loader import CatalogLoader

class SHLAgent:
    def __init__(self):
        print("🚀 Initializing SHL Agent...")
        self.catalog_loader = CatalogLoader()
        self.catalog_loader.load_catalog()
        
        if self.catalog_loader.catalog:
            self.catalog_loader.build_index()
            print(f"✅ Agent ready with {len(self.catalog_loader.catalog)} assessments!")
        else:
            print("⚠️ Agent running with empty catalog - check your data!")
        
    def process(self, messages):
        """Main entry point for processing conversations"""
        
        # Get the last user message
        last_user_msg = None
        for msg in reversed(messages):
            if msg['role'] == 'user':
                last_user_msg = msg['content']
                break
        
        if not last_user_msg:
            return self._response("Could you tell me what role you're hiring for?", [])
        
        # Check if user is ending conversation
        if self._should_end_conversation(last_user_msg):
            context = self._get_context(messages)
            search_results = self.catalog_loader.search(context, top_k=10)
            if search_results:
                return self._generate_recommendations(last_user_msg, search_results, end_conv=True)
            else:
                return self._response("Great! Let me know if you need anything else.", [], end_conversation=True)
        
        # Check if out of scope
        if self._is_out_of_scope(last_user_msg):
            return self._response(
                "I can only help with SHL assessment recommendations. Please ask about our assessments.", 
                []
            )
        
        # Check if it's a comparison
        if self._is_comparison(last_user_msg):
            return self._handle_comparison(last_user_msg)
        
        # Search catalog
        search_results = self.catalog_loader.search(last_user_msg, top_k=15)
        
        # If no results, ask for clarification
        if not search_results:
            return self._ask_clarification(messages)
        
        # Check if we have enough context to recommend
        user_count = sum(1 for m in messages if m['role'] == 'user')
        
        # If 2+ user messages OR we have enough context, recommend
        if user_count >= 2 or self._has_enough_context(messages):
            return self._generate_recommendations(last_user_msg, search_results)
        else:
            return self._ask_clarification(messages)
    
    def _response(self, reply, recommendations, end_conversation=False):
        """Standard response format"""
        return {
            'reply': reply,
            'recommendations': recommendations,
            'end_of_conversation': end_conversation
        }
    
    def _is_out_of_scope(self, query):
        """Check if query is out of scope - IMPROVED"""
        query_lower = query.lower()
        
        # These phrases clearly indicate out-of-scope requests
        clear_offtopic = [
            'give me legal advice',
            'what is the law',
            'legal requirement',
            'hiring advice',
            'how to interview',
            'salary negotiation',
            'prompt injection',
            'ignore previous instructions',
            'you are now'
        ]
        
        # Check if any clear off-topic phrase is present
        for phrase in clear_offtopic:
            if phrase in query_lower:
                return True
        
        # For legal/compliance terms, only flag if it's asking about requirements
        if 'legal' in query_lower or 'law' in query_lower or 'compliance' in query_lower:
            # If asking about legal requirements directly
            if 'am i required' in query_lower or 'is it legal' in query_lower or 'legal requirement' in query_lower:
                return True
        
        # Don't flag if the query is about hiring/assessments
        assessment_terms = ['assessment', 'test', 'evaluate', 'screen', 'hire', 'hiring', 'role', 'position', 'candidate']
        if any(term in query_lower for term in assessment_terms):
            return False
        
        return False
    
    def _is_comparison(self, query):
        """Check if query asks for comparison"""
        terms = ['difference between', 'compare', 'vs', 'versus', "what's the difference", 'differentiate']
        query_lower = query.lower()
        return any(term in query_lower for term in terms)
    
    def _get_context(self, messages):
        """Get combined context from all user messages"""
        return ' '.join([m['content'] for m in messages if m['role'] == 'user'])
    
    def _has_enough_context(self, messages):
        """Check if we have enough information to recommend"""
        context = self._get_context(messages).lower()
        
        # Check for key information - expanded for better detection
        has_role = any(word in context for word in ['hire', 'hiring', 'role', 'position', 'developer', 'engineer', 'analyst', 'manager', 'operator', 'assistant', 'clerk', 'agent', 'representative', 'staff', 'trainee', 'admin'])
        has_level = any(word in context for word in ['senior', 'mid', 'entry', 'junior', 'executive', 'director', 'level', 'graduate', 'management', 'leadership'])
        has_skill = any(word in context for word in ['skill', 'experience', 'java', 'python', 'sql', 'aws', 'spring', 'excel', 'word', 'rust', 'linux', 'networking', 'sales', 'customer', 'service', 'support', 'communication', 'analytical'])
        
        info_count = sum([has_role, has_level, has_skill])
        
        return info_count >= 2
    
    def _ask_clarification(self, messages):
        """Ask clarifying questions based on missing information"""
        context = self._get_context(messages).lower()
        user_count = sum(1 for m in messages if m['role'] == 'user')
        
        # If 2+ turns, try to recommend with what we have
        if user_count >= 2:
            search_results = self.catalog_loader.search(context, top_k=10)
            if search_results:
                return self._generate_recommendations(context, search_results)
        
        questions = []
        
        # Check what info is missing
        if 'senior' not in context and 'level' not in context and 'entry' not in context and 'mid' not in context and 'executive' not in context and 'graduate' not in context and 'leadership' not in context:
            questions.append("What's the seniority level (Entry, Mid, Senior, Executive)?")
        
        if 'skill' not in context and 'experience' not in context:
            if 'java' not in context and 'python' not in context and 'sql' not in context and 'excel' not in context and 'customer' not in context and 'service' not in context and 'communication' not in context:
                questions.append("What specific skills or experience is required?")
        
        if 'role' not in context and 'position' not in context:
            if 'hire' not in context and 'developer' not in context and 'engineer' not in context and 'manager' not in context and 'agent' not in context and 'analyst' not in context and 'admin' not in context:
                questions.append("What's the job role or position?")
        
        # If no questions to ask, try to recommend
        if not questions:
            search_results = self.catalog_loader.search(context, top_k=10)
            if search_results:
                return self._generate_recommendations(context, search_results)
            return self._response("Could you tell me more about the role and requirements?", [])
        
        reply = " ".join(questions) + " This will help me recommend the right assessments."
        
        return self._response(reply, [])
    
    def _generate_recommendations(self, query, results, end_conv=False):
        """Generate recommendations from search results"""
        top_results = results[:10]
        
        recommendations = []
        seen_names = set()
        for item in top_results:
            if isinstance(item, dict):
                name = item.get('name', '')
                if name and name not in seen_names:
                    seen_names.add(name)
                    test_types = item.get('keys', ['General'])
                    test_type = test_types[0] if test_types else 'General'
                    
                    recommendations.append({
                        'name': name,
                        'url': item.get('link', '#'),
                        'test_type': test_type
                    })
        
        if not recommendations:
            return self._response("I couldn't find specific assessments matching your criteria. Could you provide more details?", [])
        
        reply = "Based on your requirements, here are the recommended assessments:\n\n"
        
        for i, rec in enumerate(recommendations[:5], 1):
            reply += f"{i}. **{rec['name']}** ({rec['test_type']})\n"
        
        if len(recommendations) > 5:
            reply += f"\nAnd {len(recommendations)-5} more assessments that might be relevant."
        
        return self._response(reply, recommendations, end_conv)
    
    def _handle_comparison(self, query):
        """Handle product comparison requests"""
        query_lower = query.lower()
        products = []
        
        # Known product patterns
        product_patterns = {
            'OPQ': ['OPQ', 'Occupational Personality'],
            'DSI': ['DSI', 'Dependability'],
            'G+': ['G+', 'Verify'],
            'GSA': ['GSA', 'Global Skills'],
            'MQ': ['MQ', 'Motivation'],
            'UCF': ['UCF', 'Competency'],
            'Safety': ['Safety', 'Dependability'],
            '8.0': ['8.0', 'Manufacturing'],
        }
        
        # Check for each pattern
        for pattern, keywords in product_patterns.items():
            if pattern.lower() in query_lower or any(kw.lower() in query_lower for kw in keywords):
                for item in self.catalog_loader.catalog:
                    if isinstance(item, dict):
                        name = item.get('name', '')
                        if pattern.lower() in name.lower() or any(kw.lower() in name.lower() for kw in keywords):
                            if name and item not in products:
                                products.append(item)
        
        # If no pattern match, try text search
        if not products:
            words = re.findall(r'[A-Z][a-zA-Z0-9+]+', query)
            for word in words:
                for item in self.catalog_loader.catalog:
                    if isinstance(item, dict):
                        name = item.get('name', '')
                        if name and word.lower() in name.lower():
                            if item not in products:
                                products.append(item)
        
        if not products:
            return self._response(
                "I couldn't find those products in the catalog. Could you specify which assessments you'd like to compare?",
                []
            )
        
        # Build comparison
        reply = "Here's the comparison:\n\n"
        for product in products[:3]:
            name = product.get('name', 'Unknown')
            keys = product.get('keys', ['General'])
            duration = product.get('duration', 'Varies')
            desc = product.get('description', 'No description available')
            
            reply += f"**{name}**\n"
            reply += f"- Type: {', '.join(keys)}\n"
            reply += f"- Duration: {duration}\n"
            reply += f"- Description: {desc[:150]}...\n\n"
        
        # Create recommendations from the compared products
        recs = []
        for p in products[:5]:
            if isinstance(p, dict):
                recs.append({
                    'name': p.get('name', 'Unknown'),
                    'url': p.get('link', '#'),
                    'test_type': p.get('keys', ['General'])[0] if p.get('keys') else 'General'
                })
        
        return self._response(reply, recs)
    
    def _should_end_conversation(self, query):
        """Check if conversation should end based on user satisfaction"""
        end_terms = [
            'perfect', 'confirmed', 'lock it', "that's good", 'thanks', 'done',
            'good', 'great', 'excellent', 'ok', 'okay', 'yes', 'yeah',
            'that works', 'sounds good', 'perfect thanks', 'thank you',
            "that's it", "that covers it", 'good enough', 'fine',
            'works', 'got it', 'understood', 'clear', 'covers it',
            'perfect,', 'confirmed.', 'thanks.', 'good.', 'great.',
            'clear.', 'works.', 'got it.', 'understood.'
        ]
        query_lower = query.lower()
        
        if any(term in query_lower for term in end_terms):
            return True
        
        words = query_lower.split()
        if len(words) <= 3:
            positive_words = ['yes', 'ok', 'good', 'great', 'fine', 'thanks', 'done', 'sure', 'perfect', 'clear']
            if any(word in query_lower for word in positive_words):
                return True
        
        return False