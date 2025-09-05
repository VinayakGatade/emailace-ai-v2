import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { 
  Mail, 
  CheckCircle, 
  Clock, 
  AlertTriangle, 
  TrendingUp,
  Users,
  MessageSquare,
  Target,
  Loader2
} from "lucide-react";
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";
import { apiService } from "@/lib/api";

const DashboardHome = () => {
  // Fetch analytics data
  const { data: analytics, isLoading, error } = useQuery({
    queryKey: ['analytics'],
    queryFn: () => apiService.getAnalytics(),
    refetchInterval: 60000, // Refetch every minute
  });

  const summaryStats = analytics ? [
    {
      title: "Total Emails",
      value: analytics.total_emails.toString(),
      change: "+12%",
      changeType: "positive",
      icon: Mail,
      description: "all time"
    },
    {
      title: "Resolved",
      value: analytics.resolved_emails.toString(),
      change: "+8%",
      changeType: "positive", 
      icon: CheckCircle,
      description: `completion rate ${Math.round((analytics.resolved_emails / analytics.total_emails) * 100)}%`
    },
    {
      title: "Pending",
      value: analytics.pending_emails.toString(),
      change: "-5%",
      changeType: "negative",
      icon: Clock,
      description: "avg response time: 2.3h"
    },
    {
      title: "Urgent Emails",
      value: analytics.urgent_emails.toString(),
      change: "+3%",
      changeType: "positive",
      icon: AlertTriangle,
      description: "require immediate attention"
    }
  ] : [];

  const sentimentData = analytics ? [
    { name: "Positive", value: analytics.sentiment_breakdown.positive || 0, color: "hsl(var(--success))" },
    { name: "Neutral", value: analytics.sentiment_breakdown.neutral || 0, color: "hsl(var(--muted))" },
    { name: "Negative", value: analytics.sentiment_breakdown.negative || 0, color: "hsl(var(--destructive))" }
  ] : [];

  const volumeData = [
    { day: "Mon", emails: 98 },
    { day: "Tue", emails: 112 },
    { day: "Wed", emails: 127 },
    { day: "Thu", emails: 89 },
    { day: "Fri", emails: 134 },
    { day: "Sat", emails: 67 },
    { day: "Sun", emails: 45 }
  ];

  const recentActivity = [
    { action: "High priority email resolved", time: "2 minutes ago", type: "success" },
    { action: "New urgent email received", time: "5 minutes ago", type: "warning" },
    { action: "Customer satisfaction improved", time: "15 minutes ago", type: "success" },
    { action: "Response time exceeded threshold", time: "1 hour ago", type: "error" }
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin" />
        <span className="ml-2">Loading dashboard...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-destructive mb-2">Error loading dashboard</div>
        <div className="text-sm text-muted-foreground">
          {error instanceof Error ? error.message : 'Unknown error occurred'}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-muted-foreground">Welcome back! Here's your communication overview.</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {summaryStats.map((stat, index) => (
          <Card key={index} className="gradient-card shadow-medium hover:shadow-large transition-all">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {stat.title}
              </CardTitle>
              <div className="w-8 h-8 bg-accent rounded-lg flex items-center justify-center">
                <stat.icon className="w-4 h-4 text-accent-foreground" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold mb-1">{stat.value}</div>
              <div className="flex items-center space-x-2">
                <Badge 
                  variant={stat.changeType === "positive" ? "default" : "destructive"}
                  className="text-xs"
                >
                  {stat.change}
                </Badge>
                <span className="text-xs text-muted-foreground">{stat.description}</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sentiment Analysis */}
        <Card className="gradient-card shadow-medium">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <MessageSquare className="w-5 h-5" />
              <span>Sentiment Distribution</span>
            </CardTitle>
            <CardDescription>
              Customer sentiment analysis from recent emails
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={sentimentData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {sentimentData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="flex justify-center space-x-4 mt-4">
              {sentimentData.map((item, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <div 
                    className="w-3 h-3 rounded-full" 
                    style={{ backgroundColor: item.color }}
                  ></div>
                  <span className="text-sm text-muted-foreground">
                    {item.name} ({item.value}%)
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Email Volume */}
        <Card className="gradient-card shadow-medium">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="w-5 h-5" />
              <span>Weekly Email Volume</span>
            </CardTitle>
            <CardDescription>
              Email volume trends over the past week
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={volumeData}>
                  <XAxis dataKey="day" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="emails" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Quick Actions */}
        <Card className="gradient-card shadow-medium">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Target className="w-5 h-5" />
              <span>Quick Actions</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm">Response Rate</span>
              <span className="text-sm font-medium">87%</span>
            </div>
            <Progress value={87} className="h-2" />
            
            <div className="flex items-center justify-between">
              <span className="text-sm">Resolution Time</span>
              <span className="text-sm font-medium">2.3h avg</span>
            </div>
            <Progress value={65} className="h-2" />
            
            <div className="flex items-center justify-between">
              <span className="text-sm">Customer Satisfaction</span>
              <span className="text-sm font-medium">4.2/5</span>
            </div>
            <Progress value={84} className="h-2" />
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card className="lg:col-span-2 gradient-card shadow-medium">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Users className="w-5 h-5" />
              <span>Recent Activity</span>
            </CardTitle>
            <CardDescription>
              Latest updates and notifications
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivity.map((activity, index) => (
                <div key={index} className="flex items-center space-x-3 p-3 rounded-lg bg-muted/30">
                  <div className={`w-2 h-2 rounded-full ${
                    activity.type === 'success' ? 'bg-success' :
                    activity.type === 'warning' ? 'bg-warning' : 'bg-destructive'
                  }`}></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">{activity.action}</p>
                    <p className="text-xs text-muted-foreground">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default DashboardHome;