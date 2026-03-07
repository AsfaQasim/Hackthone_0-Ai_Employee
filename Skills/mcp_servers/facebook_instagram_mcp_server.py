"""
Facebook & Instagram MCP Server - Gold Tier

Integrates with Facebook Graph API and Instagram Graph API for posting and analytics.
Requires Facebook App and Business Account setup.

Setup Guide:
1. Create Facebook App at https://developers.facebook.com
2. Get Page Access Token and Instagram Business Account ID
3. Configure environment variables
"""

import logging
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from pathlib import Path
import json

from .base_mcp_server import BaseMCPServer, Tool, TextContent


class FacebookInstagramMCPServer(BaseMCPServer):
    """
    Facebook & Instagram MCP Server.

    Provides tools for posting to Facebook Pages and Instagram Business accounts,
    plus engagement analytics.
    """

    def __init__(
        self,
        name: str = "facebook_instagram_mcp_server",
        page_access_token: str = "",
        instagram_business_account_id: str = "",
        vault_path: str = "."
    ):
        """
        Initialize Facebook/Instagram MCP Server.

        Args:
            name: Server name
            page_access_token: Facebook Page Access Token
            instagram_business_account_id: Instagram Business Account ID
            vault_path: Path to vault for tracking
        """
        self.page_access_token = page_access_token
        self.instagram_business_account_id = instagram_business_account_id
        self.vault_path = Path(vault_path)
        self.tracking_dir = self.vault_path / "Social_Media_Tracking"
        self.tracking_dir.mkdir(parents=True, exist_ok=True)
        
        self.graph_api_url = "https://graph.facebook.com/v18.0"
        self.logger = logging.getLogger("FacebookInstagramMCPServer")
        
        super().__init__(name)

    def register_tools(self) -> None:
        """Register Facebook & Instagram tools."""

        # Facebook post tool
        facebook_post_tool = Tool(
            name="post_to_facebook",
            description="Create a post on Facebook Page",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Post message content"
                    },
                    "link": {
                        "type": "string",
                        "description": "Optional link to share"
                    },
                    "photo_url": {
                        "type": "string",
                        "description": "Optional photo URL to attach"
                    },
                    "scheduled_time": {
                        "type": "string",
                        "description": "Optional scheduled time (ISO 8601 format)"
                    }
                },
                "required": ["message"]
            }
        )
        self.add_tool(facebook_post_tool)

        # Instagram post tool
        instagram_post_tool = Tool(
            name="post_to_instagram",
            description="Create a post on Instagram Business account",
            inputSchema={
                "type": "object",
                "properties": {
                    "caption": {
                        "type": "string",
                        "description": "Instagram caption"
                    },
                    "image_url": {
                        "type": "string",
                        "description": "Image URL (required for Instagram posts)"
                    },
                    "is_video": {
                        "type": "boolean",
                        "description": "Is this a video post"
                    },
                    "video_url": {
                        "type": "string",
                        "description": "Video URL (if is_video is true)"
                    }
                },
                "required": ["caption", "image_url"]
            }
        )
        self.add_tool(instagram_post_tool)

        # Facebook insights tool
        facebook_insights_tool = Tool(
            name="get_facebook_insights",
            description="Get Facebook Page insights and analytics",
            inputSchema={
                "type": "object",
                "properties": {
                    "metric": {
                        "type": "string",
                        "enum": ["page_impressions", "page_engaged_users", "page_post_engagements", "page_likes", "page_reach"],
                        "description": "Metric to retrieve"
                    },
                    "period": {
                        "type": "string",
                        "enum": ["day", "week", "month", "lifetime"],
                        "description": "Time period"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days to look back"
                    }
                }
            }
        )
        self.add_tool(facebook_insights_tool)

        # Instagram insights tool
        instagram_insights_tool = Tool(
            name="get_instagram_insights",
            description="Get Instagram Business account insights",
            inputSchema={
                "type": "object",
                "properties": {
                    "metric": {
                        "type": "string",
                        "enum": ["impressions", "reach", "profile_views", "follower_count", "engagement"],
                        "description": "Metric to retrieve"
                    },
                    "period": {
                        "type": "string",
                        "enum": ["day", "week", "month"],
                        "description": "Time period"
                    }
                }
            }
        )
        self.add_tool(instagram_insights_tool)

        # Get recent posts tool
        get_posts_tool = Tool(
            name="get_facebook_posts",
            description="Get recent posts from Facebook Page",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of posts to retrieve"
                    },
                    "include_insights": {
                        "type": "boolean",
                        "description": "Include engagement metrics"
                    }
                }
            }
        )
        self.add_tool(get_posts_tool)

        # Get Instagram recent posts
        get_instagram_posts_tool = Tool(
            name="get_instagram_posts",
            description="Get recent posts from Instagram",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of posts to retrieve"
                    }
                }
            }
        )
        self.add_tool(get_instagram_posts_tool)

        # Generate summary tool
        generate_summary_tool = Tool(
            name="generate_social_media_summary",
            description="Generate summary report for Facebook and Instagram",
            inputSchema={
                "type": "object",
                "properties": {
                    "platform": {
                        "type": "string",
                        "enum": ["facebook", "instagram", "both"],
                        "description": "Platform to summarize"
                    },
                    "period_days": {
                        "type": "integer",
                        "description": "Number of days to summarize"
                    }
                }
            }
        )
        self.add_tool(generate_summary_tool)

    def _make_graph_request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        post_data: Optional[Dict[str, Any]] = None,
        method: str = "GET"
    ) -> Dict[str, Any]:
        """
        Make request to Facebook Graph API.

        Args:
            endpoint: API endpoint
            params: URL parameters
            post_data: POST data (if method is POST)
            method: HTTP method

        Returns:
            JSON response
        """
        url = f"{self.graph_api_url}/{endpoint}"
        
        if params is None:
            params = {}
        
        params['access_token'] = self.page_access_token

        try:
            if method == "GET":
                response = requests.get(url, params=params, timeout=30)
            elif method == "POST":
                response = requests.post(url, params=params, json=post_data, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            result = response.json()

            if "error" in result:
                error = result["error"]
                raise Exception(f"Graph API error: {error.get('message', 'Unknown error')} (Code: {error.get('code')})")

            return result

        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to Facebook Graph API")
        except requests.exceptions.Timeout:
            raise Exception("Facebook API request timed out")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise Exception("Invalid or expired access token")
            elif e.response.status_code == 403:
                raise Exception("Permission denied. Check app permissions.")
            raise Exception(f"HTTP error: {str(e)}")
        except Exception as e:
            raise Exception(f"Facebook API error: {str(e)}")

    def _track_post(self, platform: str, post_id: str, content: str, metadata: Dict[str, Any]):
        """Track social media post in vault"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{platform}_{timestamp}_{post_id[:8]}.md"
        filepath = self.tracking_dir / filename

        tracking_content = f"""---
platform: {platform}
post_id: {post_id}
timestamp: {datetime.now().isoformat()}
status: published
---

# {platform.title()} Post

**Posted**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Post ID**: {post_id}

## Content
{content}

## Metadata
```json
{json.dumps(metadata, indent=2)}
```

## Engagement Metrics
(Update by calling get_insights)
- Likes: 0
- Comments: 0
- Shares: 0
- Reach: 0
"""

        filepath.write_text(tracking_content, encoding='utf-8')
        self.logger.info(f"Tracked {platform} post: {filename}")

    async def handle_tool_call(self, name: str, arguments: Dict[str, Any]) -> TextContent:
        """Handle tool call requests"""
        try:
            if name == "post_to_facebook":
                return await self._post_to_facebook(arguments)
            elif name == "post_to_instagram":
                return await self._post_to_instagram(arguments)
            elif name == "get_facebook_insights":
                return await self._get_facebook_insights(arguments)
            elif name == "get_instagram_insights":
                return await self._get_instagram_insights(arguments)
            elif name == "get_facebook_posts":
                return await self._get_facebook_posts(arguments)
            elif name == "get_instagram_posts":
                return await self._get_instagram_posts(arguments)
            elif name == "generate_social_media_summary":
                return await self._generate_summary(arguments)
            else:
                return TextContent(
                    type="text",
                    text=f"Error: Unknown tool '{name}'"
                )

        except Exception as e:
            error_msg = f"Error executing {name}: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return TextContent(
                type="text",
                text=f"Error: {error_msg}"
            )

    async def _post_to_facebook(self, arguments: Dict[str, Any]) -> TextContent:
        """Post to Facebook Page"""
        message = arguments.get('message')
        link = arguments.get('link')
        photo_url = arguments.get('photo_url')
        scheduled_time = arguments.get('scheduled_time')

        # Prepare post data
        post_data = {'message': message}
        
        if link:
            post_data['link'] = link
        
        if photo_url:
            post_data['attached_media'] = [{'media_url': photo_url}]
        
        if scheduled_time:
            post_data['scheduled_publish_time'] = scheduled_time
            post_data['published'] = False

        # Post to page feed
        result = self._make_graph_request(
            f"me/feed",
            post_data=post_data,
            method="POST"
        )

        post_id = result.get('id', 'unknown')
        
        self._track_post('facebook', post_id, message, {
            'link': link,
            'photo_url': photo_url,
            'scheduled': scheduled_time is not None
        })

        status_msg = "scheduled for later" if scheduled_time else "published"
        return TextContent(
            type="text",
            text=f"Successfully {status_msg} on Facebook. Post ID: {post_id}"
        )

    async def _post_to_instagram(self, arguments: Dict[str, Any]) -> TextContent:
        """Post to Instagram Business account"""
        caption = arguments.get('caption')
        image_url = arguments.get('image_url')
        is_video = arguments.get('is_video', False)
        video_url = arguments.get('video_url')

        if not self.instagram_business_account_id:
            return TextContent(
                type="text",
                text="Error: Instagram Business Account ID not configured"
            )

        # Step 1: Create media container
        container_params = {
            'image_url': image_url if not is_video else None,
            'video_url': video_url if is_video else None,
            'caption': caption,
            'media_type': 'VIDEO' if is_video else 'IMAGE'
        }

        container_result = self._make_graph_request(
            f"{self.instagram_business_account_id}/media",
            params={k: v for k, v in container_params.items() if v is not None},
            method="POST"
        )

        creation_id = container_result.get('id')

        if not creation_id:
            return TextContent(
                type="text",
                text="Error: Failed to create Instagram media container"
            )

        # Step 2: Publish the media
        publish_result = self._make_graph_request(
            f"{self.instagram_business_account_id}/media_publish",
            params={'creation_id': creation_id},
            method="POST"
        )

        post_id = publish_result.get('id', 'unknown')
        
        self._track_post('instagram', post_id, caption, {
            'image_url': image_url,
            'video_url': video_url if is_video else None,
            'is_video': is_video
        })

        return TextContent(
            type="text",
            text=f"Successfully posted to Instagram. Post ID: {post_id}"
        )

    async def _get_facebook_insights(self, arguments: Dict[str, Any]) -> TextContent:
        """Get Facebook Page insights"""
        metric = arguments.get('metric', 'page_impressions')
        period = arguments.get('period', 'week')
        days = arguments.get('days', 7)

        # Calculate date range
        since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        until = datetime.now().strftime('%Y-%m-%d')

        result = self._make_graph_request(
            f"me/insights",
            params={
                'metric': metric,
                'period': period,
                'since': since,
                'until': until
            }
        )

        data = result.get('data', [])
        
        if not data:
            return TextContent(
                type="text",
                text=f"No insights data available for {metric}"
            )

        summary_text = f"# Facebook Insights: {metric.replace('_', ' ').title()}\n\n"
        summary_text += f"**Period**: {since} to {until}\n\n"

        for item in data:
            values = item.get('values', [])
            for value in values:
                summary_text += f"- {value.get('value', 0):,} ({value.get('end_time', 'N/A')[:10]})\n"

        return TextContent(type="text", text=summary_text)

    async def _get_instagram_insights(self, arguments: Dict[str, Any]) -> TextContent:
        """Get Instagram Business insights"""
        metric = arguments.get('metric', 'impressions')
        period = arguments.get('period', 'week')

        if not self.instagram_business_account_id:
            return TextContent(
                type="text",
                text="Error: Instagram Business Account ID not configured"
            )

        result = self._make_graph_request(
            f"{self.instagram_business_account_id}/insights",
            params={
                'metric': metric,
                'period': period
            }
        )

        data = result.get('data', [])
        
        if not data:
            return TextContent(
                type="text",
                text=f"No insights data available for {metric}"
            )

        summary_text = f"# Instagram Insights: {metric.title()}\n\n"
        
        for item in data:
            value = item.get('values', [{}])[0].get('value', 0)
            title = item.get('title', metric)
            summary_text += f"- **{title}**: {value:,}\n"

        return TextContent(type="text", text=summary_text)

    async def _get_facebook_posts(self, arguments: Dict[str, Any]) -> TextContent:
        """Get recent Facebook posts"""
        limit = arguments.get('limit', 5)
        include_insights = arguments.get('include_insights', False)

        fields = ['id', 'message', 'created_time', 'permalink_url']
        if include_insights:
            fields.extend(['likes.summary(true)', 'comments.summary(true)', 'shares'])

        result = self._make_graph_request(
            f"me/feed",
            params={
                'fields': ','.join(fields),
                'limit': limit
            }
        )

        posts = result.get('data', [])
        
        if not posts:
            return TextContent(
                type="text",
                text="No posts found on Facebook Page"
            )

        summary_text = f"# Recent Facebook Posts\n\n"
        
        for post in posts:
            message = post.get('message', 'No message')[:100]
            if len(post.get('message', '')) > 100:
                message += "..."
            
            summary_text += f"## Post: {post.get('id')}\n"
            summary_text += f"**Posted**: {post.get('created_time', 'Unknown')[:10]}\n"
            summary_text += f"**Content**: {message}\n"
            summary_text += f"**Link**: {post.get('permalink_url', 'N/A')}\n\n"

        return TextContent(type="text", text=summary_text)

    async def _get_instagram_posts(self, arguments: Dict[str, Any]) -> TextContent:
        """Get recent Instagram posts"""
        limit = arguments.get('limit', 5)

        if not self.instagram_business_account_id:
            return TextContent(
                type="text",
                text="Error: Instagram Business Account ID not configured"
            )

        result = self._make_graph_request(
            f"{self.instagram_business_account_id}/media",
            params={
                'fields': 'id,caption,media_type,media_url,permalink,timestamp',
                'limit': limit
            }
        )

        posts = result.get('data', [])
        
        if not posts:
            return TextContent(
                type="text",
                text="No posts found on Instagram"
            )

        summary_text = f"# Recent Instagram Posts\n\n"
        
        for post in posts:
            caption = post.get('caption', 'No caption')[:100]
            if len(post.get('caption', '')) > 100:
                caption += "..."
            
            summary_text += f"## Post: {post.get('id')}\n"
            summary_text += f"**Type**: {post.get('media_type', 'IMAGE')}\n"
            summary_text += f"**Posted**: {post.get('timestamp', 'Unknown')[:10]}\n"
            summary_text += f"**Caption**: {caption}\n"
            summary_text += f"**Link**: {post.get('permalink', 'N/A')}\n\n"

        return TextContent(type="text", text=summary_text)

    async def _generate_summary(self, arguments: Dict[str, Any]) -> TextContent:
        """Generate social media summary report"""
        platform = arguments.get('platform', 'both')
        period_days = arguments.get('period_days', 7)

        summary_text = f"# Social Media Summary\n\n"
        summary_text += f"**Period**: Last {period_days} days\n"
        summary_text += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        summary_text += "---\n\n"

        # Facebook summary
        if platform in ['facebook', 'both']:
            try:
                fb_posts = await self._get_facebook_posts({'limit': 10})
                fb_impressions = await self._get_facebook_insights({
                    'metric': 'page_impressions',
                    'days': period_days
                })
                fb_engagement = await self._get_facebook_insights({
                    'metric': 'page_post_engagements',
                    'days': period_days
                })

                summary_text += f"## Facebook\n\n"
                summary_text += f"{fb_impressions.text}\n\n"
                summary_text += f"{fb_engagement.text}\n\n"
            except Exception as e:
                summary_text += f"## Facebook\n\nError fetching data: {str(e)}\n\n"

        # Instagram summary
        if platform in ['instagram', 'both']:
            try:
                ig_posts = await self._get_instagram_posts({'limit': 10})
                ig_reach = await self._get_instagram_insights({
                    'metric': 'reach',
                    'period': 'week'
                })
                ig_followers = await self._get_instagram_insights({
                    'metric': 'follower_count',
                    'period': 'week'
                })

                summary_text += f"## Instagram\n\n"
                summary_text += f"{ig_reach.text}\n\n"
                summary_text += f"{ig_followers.text}\n\n"
            except Exception as e:
                summary_text += f"## Instagram\n\nError fetching data: {str(e)}\n\n"

        summary_text += f"\n---\n\n*Generated by Facebook/Instagram MCP Server v1.0*\n"

        return TextContent(type="text", text=summary_text)


# Example usage
if __name__ == "__main__":
    import asyncio
    import os
    from dotenv import load_dotenv

    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    async def test_social_media_server():
        """Test Facebook/Instagram MCP Server"""
        server = FacebookInstagramMCPServer(
            page_access_token=os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', ''),
            instagram_business_account_id=os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID', '')
        )

        # List tools
        print("Available tools:")
        for tool in server.list_tools():
            print(f"  - {tool['name']}: {tool['description']}")

        # Test get posts
        try:
            result = await server.execute_tool("get_facebook_posts", {"limit": 3})
            print(f"\nFacebook Posts: {result.text}")
        except Exception as e:
            print(f"\nError: {e}")

    asyncio.run(test_social_media_server())
