import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Search, Filter, Flame, Clock, CheckCircle, AlertTriangle, Loader2 } from "lucide-react";
import { apiService, Email } from "@/lib/api";

const Inbox = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState("date");

  // Fetch emails from API
  const { data: emails = [], isLoading, error } = useQuery({
    queryKey: ['emails'],
    queryFn: () => apiService.getEmails(),
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case "urgent":
      case "high":
        return <Flame className="w-4 h-4 text-destructive" />;
      case "normal":
        return <AlertTriangle className="w-4 h-4 text-warning" />;
      default:
        return <Clock className="w-4 h-4 text-muted-foreground" />;
    }
  };

  const getSentimentBadge = (sentiment: string) => {
    const variants = {
      positive: "default",
      neutral: "secondary", 
      negative: "destructive"
    } as const;

    return (
      <Badge variant={variants[sentiment as keyof typeof variants]}>
        {sentiment}
      </Badge>
    );
  };

  const getStatusIcon = (status: string) => {
    return status === "resolved" ? (
      <CheckCircle className="w-4 h-4 text-success" />
    ) : (
      <Clock className="w-4 h-4 text-warning" />
    );
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.abs(now.getTime() - date.getTime()) / (1000 * 60 * 60);
    
    if (diffInHours < 24) {
      return `${Math.floor(diffInHours)}h ago`;
    }
    return date.toLocaleDateString();
  };

  // Filter and sort emails
  const filteredEmails = emails
    .filter(email =>
      email.sender.toLowerCase().includes(searchQuery.toLowerCase()) ||
      email.subject.toLowerCase().includes(searchQuery.toLowerCase())
    )
    .sort((a, b) => {
      switch (sortBy) {
        case "priority":
          const priorityOrder = { urgent: 0, high: 1, normal: 2, low: 3 };
          return priorityOrder[a.priority as keyof typeof priorityOrder] - priorityOrder[b.priority as keyof typeof priorityOrder];
        case "sender":
          return a.sender.localeCompare(b.sender);
        case "status":
          return a.status.localeCompare(b.status);
        case "date":
        default:
          return new Date(b.date).getTime() - new Date(a.date).getTime();
      }
    });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin" />
        <span className="ml-2">Loading emails...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-destructive mb-2">Error loading emails</div>
        <div className="text-sm text-muted-foreground">
          {error instanceof Error ? error.message : 'Unknown error occurred'}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold mb-2">Inbox</h1>
          <p className="text-muted-foreground">Manage and respond to customer communications</p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge variant="outline" className="flex items-center space-x-1">
            <Clock className="w-3 h-3" />
            <span>{filteredEmails.filter(e => e.status === "pending").length} Pending</span>
          </Badge>
          <Badge variant="outline" className="flex items-center space-x-1">
            <Flame className="w-3 h-3" />
            <span>{filteredEmails.filter(e => e.priority === "urgent" || e.priority === "high").length} Urgent</span>
          </Badge>
        </div>
      </div>

      {/* Filters */}
      <Card className="gradient-card shadow-medium">
        <CardHeader>
          <CardTitle className="text-lg">Filter & Search</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
              <Input
                placeholder="Search emails by sender or subject..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="w-full md:w-48">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="date">Latest First</SelectItem>
                <SelectItem value="priority">Priority</SelectItem>
                <SelectItem value="sender">Sender</SelectItem>
                <SelectItem value="status">Status</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline" className="flex items-center space-x-2">
              <Filter className="w-4 h-4" />
              <span>More Filters</span>
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Email Table */}
      <Card className="gradient-card shadow-medium">
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-12">Priority</TableHead>
                <TableHead>Sender</TableHead>
                <TableHead>Subject</TableHead>
                <TableHead>Sentiment</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="w-12"></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredEmails.map((email) => (
                <TableRow 
                  key={email.id}
                  className="cursor-pointer hover:bg-muted/30 transition-colors"
                  onClick={() => navigate(`/dashboard/email/${email.id}`)}
                >
                  <TableCell>
                    {getPriorityIcon(email.priority)}
                  </TableCell>
                  <TableCell className="font-medium">
                    <div>
                      <p className="text-sm font-medium">{email.sender}</p>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div>
                      <p className="font-medium text-sm mb-1">{email.subject}</p>
                      <p className="text-xs text-muted-foreground line-clamp-1">
                        {email.summary || email.body.substring(0, 100) + "..."}
                      </p>
                    </div>
                  </TableCell>
                  <TableCell>
                    {getSentimentBadge(email.sentiment)}
                  </TableCell>
                  <TableCell className="text-sm text-muted-foreground">
                    {formatDate(email.date)}
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center space-x-2">
                      {getStatusIcon(email.status)}
                      <span className="text-sm capitalize">{email.status}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="w-2 h-2 rounded-full bg-primary"></div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {filteredEmails.length === 0 && (
        <Card className="gradient-card shadow-medium">
          <CardContent className="text-center py-12">
            <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto mb-4">
              <Search className="w-8 h-8 text-muted-foreground" />
            </div>
            <h3 className="text-lg font-medium mb-2">No emails found</h3>
            <p className="text-muted-foreground">
              Try adjusting your search criteria or filters
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default Inbox;