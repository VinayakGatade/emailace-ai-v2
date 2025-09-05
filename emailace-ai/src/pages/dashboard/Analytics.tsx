import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  AreaChart,
  Area
} from "recharts";
import { 
  TrendingUp, 
  TrendingDown, 
  MessageSquare, 
  Clock, 
  Users, 
  Target,
  Download,
  Calendar,
  BarChart3,
  Loader2
} from "lucide-react";
import { apiService } from "@/lib/api";

const Analytics = () => {
  // Fetch analytics data
  const { data: analytics, isLoading, error } = useQuery({
    queryKey: ['analytics'],
    queryFn: () => apiService.getAnalytics(),
    refetchInterval: 60000, // Refetch every minute
  });

  const sentimentData = analytics ? [
    { name: "Positive", value: analytics.sentiment_breakdown.positive || 0, color: "hsl(var(--success))" },
    { name: "Neutral", value: analytics.sentiment_breakdown.neutral || 0, color: "hsl(var(--muted-foreground))" },
    { name: "Negative", value: analytics.sentiment_breakdown.negative || 0, color: "hsl(var(--destructive))" }
  ] : [];

  const urgencyData = analytics ? [
    { name: "Urgent", value: analytics.priority_breakdown.urgent || 0, urgent: analytics.priority_breakdown.urgent || 0, notUrgent: 0 },
    { name: "High", value: analytics.priority_breakdown.high || 0, urgent: analytics.priority_breakdown.high || 0, notUrgent: 0 },
    { name: "Normal", value: analytics.priority_breakdown.normal || 0, urgent: 0, notUrgent: analytics.priority_breakdown.normal || 0 },
    { name: "Low", value: analytics.priority_breakdown.low || 0, urgent: 0, notUrgent: analytics.priority_breakdown.low || 0 }
  ] : [];

  const volumeOverTime = [
    { date: "Jan 1", emails: 45, resolved: 38 },
    { date: "Jan 2", emails: 52, resolved: 47 },
    { date: "Jan 3", emails: 48, resolved: 41 },
    { date: "Jan 4", emails: 61, resolved: 55 },
    { date: "Jan 5", emails: 55, resolved: 48 },
    { date: "Jan 6", emails: 67, resolved: 62 },
    { date: "Jan 7", emails: 71, resolved: 64 },
    { date: "Jan 8", emails: 58, resolved: 52 },
    { date: "Jan 9", emails: 63, resolved: 58 },
    { date: "Jan 10", emails: 69, resolved: 61 },
    { date: "Jan 11", emails: 75, resolved: 68 },
    { date: "Jan 12", emails: 82, resolved: 74 },
    { date: "Jan 13", emails: 78, resolved: 71 },
    { date: "Jan 14", emails: 85, resolved: 78 }
  ];

  const responseTimeData = [
    { time: "< 1h", count: 45 },
    { time: "1-2h", count: 62 },
    { time: "2-4h", count: 38 },
    { time: "4-8h", count: 24 },
    { time: "> 8h", count: 12 }
  ];

  const kpis = analytics ? [
    {
      title: "Avg Response Time",
      value: "2.3h",
      change: "-12%",
      changeType: "positive",
      icon: Clock,
      description: "vs last week"
    },
    {
      title: "Resolution Rate",
      value: `${Math.round((analytics.resolved_emails / analytics.total_emails) * 100)}%`,
      change: "+5%", 
      changeType: "positive",
      icon: Target,
      description: "this week"
    },
    {
      title: "Customer Satisfaction",
      value: "4.2/5",
      change: "+0.3",
      changeType: "positive",
      icon: Users,
      description: "average rating"
    },
    {
      title: "Total Volume",
      value: analytics.total_emails.toString(),
      change: "+18%",
      changeType: "neutral",
      icon: MessageSquare,
      description: "emails total"
    }
  ] : [];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin" />
        <span className="ml-2">Loading analytics...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-destructive mb-2">Error loading analytics</div>
        <div className="text-sm text-muted-foreground">
          {error instanceof Error ? error.message : 'Unknown error occurred'}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold mb-2">Analytics</h1>
          <p className="text-muted-foreground">
            Insights and performance metrics for your communication workflow
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm">
            <Calendar className="w-4 h-4 mr-2" />
            Last 30 days
          </Button>
          <Button variant="outline" size="sm">
            <Download className="w-4 h-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {kpis.map((kpi, index) => (
          <Card key={index} className="gradient-card shadow-medium hover:shadow-large transition-all">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {kpi.title}
              </CardTitle>
              <div className="w-8 h-8 bg-accent rounded-lg flex items-center justify-center">
                <kpi.icon className="w-4 h-4 text-accent-foreground" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold mb-1">{kpi.value}</div>
              <div className="flex items-center space-x-2">
                <div className="flex items-center">
                  {kpi.changeType === "positive" ? (
                    <TrendingUp className="w-3 h-3 text-success mr-1" />
                  ) : kpi.changeType === "negative" ? (
                    <TrendingDown className="w-3 h-3 text-destructive mr-1" />
                  ) : null}
                  <Badge 
                    variant={kpi.changeType === "positive" ? "default" : 
                            kpi.changeType === "negative" ? "destructive" : "secondary"}
                    className="text-xs"
                  >
                    {kpi.change}
                  </Badge>
                </div>
                <span className="text-xs text-muted-foreground">{kpi.description}</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sentiment Distribution */}
        <Card className="gradient-card shadow-medium">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <MessageSquare className="w-5 h-5" />
              <span>Sentiment Analysis</span>
            </CardTitle>
            <CardDescription>
              Customer sentiment distribution over time
            </CardDescription>
          </CardHeader>
          <CardContent>
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

        {/* Urgency Breakdown */}
        <Card className="gradient-card shadow-medium">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <BarChart3 className="w-5 h-5" />
              <span>Priority Distribution</span>
            </CardTitle>
            <CardDescription>
              Email urgency levels and handling
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={urgencyData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="urgent" stackId="a" fill="hsl(var(--destructive))" name="Urgent" />
                  <Bar dataKey="notUrgent" stackId="a" fill="hsl(var(--primary))" name="Not Urgent" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Email Volume Over Time */}
      <Card className="gradient-card shadow-medium">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="w-5 h-5" />
            <span>Email Volume Trends</span>
          </CardTitle>
          <CardDescription>
            Daily email volume and resolution rates over the past two weeks
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={volumeOverTime}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Area 
                  type="monotone" 
                  dataKey="emails" 
                  stackId="1" 
                  stroke="hsl(var(--primary))" 
                  fill="hsl(var(--primary))" 
                  fillOpacity={0.6}
                  name="Total Emails"
                />
                <Area 
                  type="monotone" 
                  dataKey="resolved" 
                  stackId="2" 
                  stroke="hsl(var(--success))" 
                  fill="hsl(var(--success))" 
                  fillOpacity={0.6}
                  name="Resolved"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Response Time Distribution */}
        <Card className="gradient-card shadow-medium">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Clock className="w-5 h-5" />
              <span>Response Time Distribution</span>
            </CardTitle>
            <CardDescription>
              How quickly we respond to customer emails
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={responseTimeData} layout="horizontal">
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" />
                  <YAxis dataKey="time" type="category" />
                  <Tooltip />
                  <Bar dataKey="count" fill="hsl(var(--accent))" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Performance Summary */}
        <Card className="gradient-card shadow-medium">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Target className="w-5 h-5" />
              <span>Performance Summary</span>
            </CardTitle>
            <CardDescription>
              Key metrics for this reporting period
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium">First Response Rate</span>
                <span className="text-sm">94%</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div className="bg-success h-2 rounded-full w-[94%]"></div>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium">Resolution Rate</span>
                <span className="text-sm">87%</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div className="bg-primary h-2 rounded-full w-[87%]"></div>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium">Customer Satisfaction</span>
                <span className="text-sm">4.2/5</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div className="bg-accent h-2 rounded-full w-[84%]"></div>
              </div>
            </div>
            
            <div className="pt-4 border-t">
              <div className="text-sm text-muted-foreground mb-2">Top Issues This Week</div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Server Issues</span>
                  <Badge variant="destructive">32</Badge>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Feature Requests</span>
                  <Badge variant="default">28</Badge>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Account Issues</span>
                  <Badge variant="secondary">15</Badge>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Analytics;